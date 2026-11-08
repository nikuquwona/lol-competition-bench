"""Redact local POSIX account names in ls -l rows without changing event lines."""

import re
import hashlib
import json
from pathlib import Path

# Match the complete metadata prefix to avoid rewriting commands, player names or normal prose.
LONG_LISTING = re.compile(
    rb"(?P<mode>[-bcdlps][rwxSsTt-]{9}[@+.]?[ \t]+[0-9]+[ \t]+)"
    rb"(?P<owner>[a-zA-Z_][a-zA-Z0-9_.-]*)(?P<gap>[ \t]+)"
    rb"(?P<group>[a-zA-Z_][a-zA-Z0-9_.-]*)(?=[ \t]+[0-9])"
)


def strip_accounts(data):
    def replace(match):
        if match["owner"] in (b"root", b"daemon", b"nobody") and match["group"] in (
            b"root",
            b"wheel",
            b"daemon",
            b"nogroup",
        ):
            return match[0]
        return match["mode"] + b"[local-user]" + match["gap"] + b"[local-group]"

    return LONG_LISTING.sub(replace, data)


def stage_accounts(source, target, planned, filenames, previous_public=None):
    """If needed, project immutable organizer artifacts into a clean public shard."""
    files = [Path("report.json")]
    files += [
        Path("jobs") / task / name
        for task in planned
        for name in filenames
        if (source / "jobs" / task / name).is_file()
    ]
    changes = {}
    for rel in files:
        src = source / rel
        if src.is_symlink() or not src.resolve().is_relative_to(source.resolve()):
            raise ValueError("Unsafe source artifact")
        raw = src.read_bytes()
        clean = strip_accounts(raw)
        if clean != raw:
            changes[rel] = clean
    if not changes:
        return source
    receipts = {}
    inherited = source / "redactions.json"
    if inherited.exists():
        receipts = json.loads(inherited.read_bytes())
    for rel in files:
        raw = (source / rel).read_bytes()
        clean = changes.get(rel, raw)
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(clean)
        if rel in changes:
            previous = hashlib.sha256(raw).hexdigest()
            prior = receipts.get(rel.as_posix(), {})
            if prior and prior["public_sha256"] != previous:
                raise ValueError(
                    "Prior redaction proof does not match its source artifact"
                )
            published = previous_public / rel if previous_public is not None else None
            evidence_key = "input_to_account_filter_sha256"
            if published is not None and published.is_file():
                if hashlib.sha256(published.read_bytes()).hexdigest() == previous:
                    evidence_key = "prior_public_sha256"
            receipts[rel.as_posix()] = {
                "original_sha256": prior.get("original_sha256", previous),
                evidence_key: previous,
                "public_sha256": hashlib.sha256(clean).hexdigest(),
            }
    (target / "redactions.json").write_text(json.dumps(receipts, indent=2) + "\n")
    return target
