"""Conservative static descriptions of forecast IO in native shell transcripts."""

import ast
from dataclasses import dataclass
import json
import re
import shlex

from production.score import FIELDS, unique_fields


def forecast(text, *, python_repr=False):
    """Accept one complete probability object. Do not search prose for matching braces."""
    if not isinstance(text, str) or len(text) > 4096:
        return None
    try:
        if python_repr:
            obj = ast.parse(text.strip(), mode="eval").body
            if not isinstance(obj, ast.Dict) or len(obj.keys) != len(FIELDS):
                return None
            value = ast.literal_eval(obj)
        else:
            value = json.loads(text, object_pairs_hook=unique_fields)
    except (SyntaxError, ValueError, TypeError, RecursionError):
        return None
    if (
        isinstance(value, dict)
        and set(value) == set(FIELDS)
        and all(type(x) in (int, float) and 0 <= x <= 1 for x in value.values())
    ):
        return value
    return None


PATH_PREFIX = r"(?:\./|/app/|\[ephemeral\]/app/)?"
SNAP = PATH_PREFIX + r"snapshot\.json"
PRED = PATH_PREFIX + r"prediction\.json"


def read_open(node, filename):
    if (
        not isinstance(node, ast.Call)
        or not isinstance(node.func, ast.Name)
        or node.func.id != "open"
        or node.keywords
    ):
        return False
    return (
        len(node.args) in (1, 2)
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        and re.fullmatch(filename, node.args[0].value)
        and (
            len(node.args) == 1
            or isinstance(node.args[1], ast.Constant)
            and node.args[1].value == "r"
        )
    )


def json_load(node):
    return (
        isinstance(node, ast.Call)
        and ast.unparse(node.func) == "json.load"
        and len(node.args) == 1
        and not node.keywords
    )


def opens_snapshot(body):
    """Only attest a top-level unconditional open/read, before arbitrary program logic."""
    for stmt in body:
        if isinstance(stmt, ast.Import) and all(
            a.name == "json" and not a.asname for a in stmt.names
        ):
            continue
        if isinstance(stmt, ast.With) and len(stmt.items) == 1:
            entry = stmt.items[0]
            if not read_open(entry.context_expr, SNAP) or not isinstance(
                entry.optional_vars, ast.Name
            ):
                return False
            first = stmt.body[0]
            if isinstance(first, ast.Assign) and json_load(first.value):
                arg = first.value.args[0]
                return isinstance(arg, ast.Name) and arg.id == entry.optional_vars.id
            return False
        if isinstance(stmt, ast.Assign) and json_load(stmt.value):
            return bool(read_open(stmt.value.args[0], SNAP))
        break
    return False


@dataclass
class Evidence:
    snapshot: bool = False
    writes: bool = False
    # False invalidates a previous observation, even if the tool later errors.
    read_only: bool = False
    values: dict | None = None
    known: bool = True
    kind: str | None = None


def readback_validator(tree, output):
    """Bind a complete stdout layout to a straight-line file read; ignore arbitrary prose."""
    unknown = Evidence(known=False)
    variables = set()
    borrowed = set()
    for statement in tree.body:
        if isinstance(statement, ast.With):
            for entry in statement.items:
                if not read_open(entry.context_expr, PRED) or not isinstance(
                    entry.optional_vars, ast.Name
                ):
                    return unknown
                borrowed.add(entry.optional_vars.id)
    if not any(isinstance(n, ast.Call) and read_open(n, PRED) for n in ast.walk(tree)):
        return unknown
    pure = {"json.load", "json.dumps", "print", "set", "all", "isinstance"}
    for n in ast.walk(tree):
        if isinstance(n, ast.stmt) and not isinstance(
            n, (ast.Import, ast.Assign, ast.Expr, ast.Assert, ast.For, ast.With)
        ):
            return unknown
        if isinstance(n, ast.Import) and any(
            a.name != "json" or a.asname for a in n.names
        ):
            return unknown
        if isinstance(n, ast.Assign):
            if (
                len(n.targets) != 1
                or not isinstance(n.targets[0], ast.Name)
                or not json_load(n.value)
            ):
                return unknown
            source = n.value.args[0]
            if not read_open(source, PRED) and not (
                isinstance(source, ast.Name) and source.id in borrowed
            ):
                return unknown
            variables.add(n.targets[0].id)
        if isinstance(n, ast.For):
            if not all(
                isinstance(t, (ast.Name, ast.Tuple, ast.Store))
                for t in ast.walk(n.target)
            ):
                return unknown
            if any(
                isinstance(t, ast.Name) and t.id in variables
                for t in ast.walk(n.target)
            ):
                return unknown
        if isinstance(n, ast.Call):
            name = ast.unparse(n.func)
            if name == "open":
                if not read_open(n, PRED):
                    return unknown
            elif name not in pure and not (
                isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id in variables
                and n.func.attr in ("values", "items")
            ):
                return unknown
        if (
            isinstance(n, (ast.NamedExpr, ast.Lambda, ast.Delete, ast.Starred))
            or isinstance(n, ast.Attribute)
            and n.attr.startswith("__")
        ):
            return unknown

    # Limited grammar for stdout permits verifier messages before/after the file value.
    lines = []
    payload = r"(?P<value>\{[^{}]{1,2048}\})"
    for statement in tree.body:
        if not isinstance(statement, ast.Expr) or not isinstance(
            statement.value, ast.Call
        ):
            continue
        expr = statement.value
        if ast.unparse(expr.func) != "print" or expr.keywords:
            continue
        parts = []
        for arg in expr.args:
            if isinstance(arg, ast.Name) and arg.id in variables:
                parts.append(payload)
            elif (
                isinstance(arg, ast.Call)
                and ast.unparse(arg.func) == "json.dumps"
                and arg.args
                and json_load(arg.args[0])
                and read_open(arg.args[0].args[0], PRED)
            ):
                parts.append(payload)
            elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                parts.append(re.escape(arg.value))
            elif isinstance(arg, ast.Call) and ast.unparse(arg.func) == "all":
                parts.append(r"(?:True|False)")
            else:
                return Evidence(read_only=True)
        lines.append(" ".join(parts))
    layout = "\n".join(lines)
    if layout.count(payload) == 1 and (match := re.fullmatch(layout, output.strip())):
        return Evidence(
            read_only=True,
            values=forecast(match["value"], python_repr=True),
            kind="readback",
        )
    return Evidence(read_only=True)


def literal_python_write(tree, output):
    """Match small scripts with one literal forecast, one actual write and optional reporting."""
    code = "\n".join(ast.unparse(stmt) for stmt in tree.body)
    match = re.fullmatch(
        r"import json\n(?P<v>[A-Za-z_]\w*) = (?P<data>\{[^\n{}]+\})\n"
        r"(?:json\.dump\((?P=v), open\('" + PRED + r"', 'w'\)\)"
        r"|with open\('"
        + PRED
        + r"', 'w'\) as (?P<f>\w+):\n    json\.dump\((?P=v), (?P=f)\))"
        r"(?:\n(?P<after>.*))?",
        code,
        re.S,
    )
    if not match or match["v"] in {"json", "open", "print"}:
        return None
    source = match["after"] or ""
    literal = forecast(match["data"], python_repr=True)
    # Known harmless labels may precede the final print.
    label = re.match(r"^print\('([A-Za-z .:_]+)'\)\n", source)
    if label:
        source = source[label.end() :]
        if not output.startswith(label[1] + "\n"):
            return Evidence(writes=True)
        output = output.removeprefix(label[1] + "\n")
    if re.fullmatch(r"print\(open\('" + PRED + r"'\)\.read\(\)\)", source):
        kind = "readback"
    elif re.fullmatch(
        r"print\((?:"
        + match["v"]
        + r"|json\.dumps\("
        + match["v"]
        + r"(?:, indent=2)?\))\)",
        source,
    ):
        kind = "reported_write"
    else:
        return Evidence(writes=True, known=not source)
    return Evidence(
        writes=True,
        values=literal
        if literal == forecast(output, python_repr=kind == "reported_write")
        else None,
        kind=kind,
    )


def python_evidence(source, output):
    try:
        tree = ast.parse(source)
    except (ValueError, SyntaxError):
        return Evidence(known=False)
    if opens_snapshot(tree.body):
        return Evidence(snapshot=True, known=False)
    return literal_python_write(tree, output) or readback_validator(tree, output)


def shell_evidence(raw, output):
    """A small positive grammar for observed IO. Unknown shell never certifies a file."""
    command = raw.strip()
    try:
        if re.match(r"^/bin/(?:z|ba)?sh -l?c ", command):
            wrapped = shlex.split(command)
            if len(wrapped) != 3:
                return Evidence(known=False)
            command = wrapped[2].strip()
        if re.search(r"\$[\w({]|\x60", command):
            return Evidence(known=False)
        command = re.sub(r"^ls -la && ", "", command, count=1)
        if re.fullmatch(
            r"cat " + SNAP + r"(?:\s*\|\s*head -(?:c ?|n ?)?\d+)?", command
        ):
            return Evidence(snapshot=True, read_only=True)
        if re.fullmatch(r"cat " + PRED, command):
            return Evidence(read_only=True, values=forecast(output), kind="readback")
        # Quoted heredoc payloads are literal. Never trust an unrelated echo as readback.
        write = re.fullmatch(
            r"cat\s*>\s*"
            + PRED
            + r"\s*<<\s*'(?P<end>\w+)'\s*\n(?P<data>.*?)\n(?P=end)(?:\n(?P<tail>.*))?",
            command,
            re.S,
        )
        if write:
            literal = forecast(write["data"])
            tail = write["tail"] or ""
            notice = re.match(r'^echo "([A-Za-z .:_]+)"\n', tail)
            if notice:
                if not output.startswith(notice[1] + "\n"):
                    return Evidence(writes=True)
                tail = tail[notice.end() :]
                output = output.removeprefix(notice[1] + "\n")
            if re.fullmatch(r"cat " + PRED, tail):
                return Evidence(
                    writes=True,
                    values=literal if literal == forecast(output) else None,
                    kind="readback",
                )
            if tail.startswith("python3 -c ") and literal:
                verified = shell_evidence(tail, output)
                if verified.kind == "readback" and verified.values == literal:
                    return Evidence(writes=True, values=literal, kind="readback")
            return Evidence(writes=True, known=False)
        if re.fullmatch(r"echo '[^'\\n]+'\\s*>\\s*" + PRED, command):
            return Evidence(writes=True)
        py = re.fullmatch(
            r"python3? - <<\s*'(?P<end>\w+)'\s*\n(?P<code>.*?)\n(?P=end)", command, re.S
        )
        if py:
            return python_evidence(py["code"], output)
        words = shlex.split(command)
        if len(words) == 3 and words[:2] in (["python3", "-c"], ["python", "-c"]):
            return python_evidence(words[2], output)
        if (
            words
            and words[0] in ("ls", "pwd")
            and re.fullmatch(r"[\w./\[\] -]+", command)
        ):
            return Evidence(read_only=True)
    except (ValueError, TypeError, RecursionError):
        pass
    return Evidence(known=False)
