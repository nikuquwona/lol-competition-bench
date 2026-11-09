"""Read the model requests and responses recorded at the controlled inference gateway."""

import base64
import hashlib
import json
from functools import lru_cache

MAX_LINE = 6 * 1024 * 1024
MAX_FILE = 34 * 1024 * 1024


@lru_cache(maxsize=48)
def _scan(path, stamp, size):
    if size > MAX_FILE:
        raise ValueError("Model context exceeds the artifact size limit")
    calls = {}
    with path.open("rb") as stream:
        while stream.tell() < size:
            offset = stream.tell()
            line = stream.readline(min(MAX_LINE + 1, size - offset))
            if len(line) > MAX_LINE:
                raise ValueError("Oversize model context record")
            # A live writer may still be appending the last record.
            if not line.endswith(b"\n"):
                break
            row = json.loads(line)
            key = row["call_id"]
            part = row["type"]
            if (
                type(key) is not int
                or key < 1
                or part not in ("request", "response")
                or row["schema_version"] != 1
            ):
                raise ValueError("Invalid model context record")
            parts = calls.setdefault(key, {})
            if part in parts:
                raise ValueError("Duplicate model context record")
            # Only offsets and display metadata belong in the shared index cache.
            parts[part] = (
                offset,
                len(line),
                {
                    k: row.get(k)
                    for k in (
                        "source",
                        "provider",
                        "route",
                        "model",
                        "status",
                        "content_type",
                        "timestamp",
                        "state",
                        "body_bytes",
                        "truncated",
                        "withheld",
                    )
                },
            )
    if any("request" not in pair for pair in calls.values()):
        raise ValueError("Model response without its request")
    return calls


def _body(stream, record):
    offset, length, _ = record
    stream.seek(offset)
    row = json.loads(stream.read(length))
    data = base64.b64decode(row["body_b64"], validate=True)
    if len(data) != row["captured_bytes"] or (
        not row["truncated"] and hashlib.sha256(data).hexdigest() != row["sha256"]
    ):
        raise ValueError("Model context body failed its integrity check")
    return data.decode("utf-8", errors="replace")


def model_context(path, call_id=None):
    st = path.stat()
    calls = _scan(path, st.st_mtime_ns, st.st_size)
    if call_id is not None and call_id not in calls:
        raise KeyError(call_id)
    summaries = []
    for key in [call_id] if call_id is not None else sorted(calls):
        pair = calls[key]
        req = pair["request"][2]
        res = pair["response"][2] if "response" in pair else {}
        item = {
            k: req[k] for k in ("source", "provider", "route", "model", "timestamp")
        }
        item.update(
            id=key,
            status=res.get("status"),
            state=res.get("state", "response_unrecorded"),
            response_at=res.get("timestamp"),
            content_type=res.get("content_type"),
            request_bytes=req["body_bytes"],
            response_bytes=res.get("body_bytes"),
            request_truncated=bool(req["truncated"]),
            response_truncated=bool(res.get("truncated")),
            request_withheld=req.get("withheld"),
            response_withheld=res.get("withheld"),
            complete=(
                res.get("state") in ("complete", "http_error")
                and not any(
                    (
                        req["truncated"],
                        res.get("truncated"),
                        req["withheld"],
                        res.get("withheld"),
                    )
                )
            ),
        )
        if call_id is None:
            summaries.append(item)
            continue
        with path.open("rb") as stream:
            request_text = _body(stream, pair["request"])
            item["request"] = (
                None
                if req["truncated"] or req["withheld"]
                else json.loads(request_text)
            )
            if item["request"] is None:
                item["request_excerpt"] = request_text
            item["response"] = (
                _body(stream, pair["response"]) if "response" in pair else ""
            )
        return item
    return {"format": "model-context-v1", "calls": summaries}
