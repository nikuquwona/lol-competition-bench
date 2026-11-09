"""Private, bounded HTTP entity-body journal. No headers or credentials are serialized."""

import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import threading
from urllib.parse import quote

FILENAME = "model-context.jsonl"
BODY_LIMIT = 4 * 1024 * 1024
TRIAL_LIMIT = 24 * 1024 * 1024


def create_private_file(path):
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
    os.close(fd)


def credential_patterns(values):
    forms = set()
    for value in values:
        if not value:
            continue
        raw = value.encode()
        forms.update(
            (
                raw,
                json.dumps(value)[1:-1].encode(),
                quote(value, safe="").encode(),
                base64.b64encode(raw),
                base64.urlsafe_b64encode(raw),
            )
        )
    return tuple(forms)


class Body:
    def __init__(self):
        self.digest = hashlib.sha256()
        self.size = 0
        self.prefix = bytearray()
        self.tail = b""
        self.capped = False
        self.withheld = False

    def observe(self, data, log):
        self.digest.update(data)
        self.size += len(data)
        if self.withheld:
            return
        if log.secrets:
            window = self.tail + data
            if any(secret in window for secret in log.secrets):
                log.remaining += len(self.prefix)
                self.prefix.clear()
                self.tail = b""
                self.withheld = True
                return
            self.tail = window[-log.overlap :] if log.overlap else b""
        if not self.capped:
            n = min(len(data), log.body_limit - len(self.prefix), log.remaining)
            self.prefix.extend(data[:n])
            log.remaining -= n
            self.capped = n < len(data)

    def record(self):
        result = {
            "body_b64": base64.b64encode(self.prefix).decode("ascii"),
            "body_bytes": self.size,
            "captured_bytes": len(self.prefix),
            "sha256": self.digest.hexdigest(),
            "truncated": len(self.prefix) != self.size,
        }
        if self.withheld:
            result["withheld"] = "credential_echo"
        return result


class Exchange:
    def __init__(self, log, call_id):
        self.log = log
        self.call_id = call_id
        self.body = Body()
        self.status = None
        self.content_type = None

    def head(self, status, content_type):
        # Limit the journal to the media type. Arbitrary response headers are never copied.
        mime = (content_type or "").split(";", 1)[0].strip().lower()
        with self.log.lock:
            self.status = status
            self.content_type = (
                mime
                if re.fullmatch(r"[a-z0-9.+-]{1,64}/[a-z0-9.+-]{1,64}", mime)
                else None
            )

    def append(self, data):
        with self.log.lock:
            if self.call_id in self.log.pending:
                self.body.observe(data, self.log)

    def finish(self, state=None):
        with self.log.lock:
            if self.log.pending.pop(self.call_id, None) is None:
                return
            if state is None:
                state = (
                    "complete"
                    if self.status is not None and 200 <= self.status < 300
                    else "http_error"
                )
            self.log.write(
                "response",
                self.call_id,
                **self.body.record(),
                status=self.status,
                content_type=self.content_type,
                state=state,
            )


class WireLog:
    def __init__(
        self,
        path,
        *,
        secrets=(),
        existing_empty=False,
        body_limit=BODY_LIMIT,
        trial_limit=TRIAL_LIMIT,
    ):
        path = Path(path)
        if not existing_empty:
            create_private_file(path)
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_NOFOLLOW)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size or info.st_mode & 0o077:
            os.close(fd)
            raise ValueError("Expected empty owner-only regular context log")
        self.stream = os.fdopen(fd, "wb")
        self.lock = threading.RLock()
        self.pending = {}
        self.sequence = 0
        self.remaining = trial_limit
        self.body_limit = body_limit
        self.secrets = credential_patterns(secrets)
        self.overlap = max((len(s) - 1 for s in self.secrets), default=0)

    def write(self, kind, call_id, **fields):
        row = {
            "schema_version": 1,
            "type": kind,
            "call_id": call_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **fields,
        }
        self.stream.write(json.dumps(row, separators=(",", ":")).encode() + b"\n")
        self.stream.flush()

    def start(self, provider, route, model, raw):
        with self.lock:
            if self.stream.closed:
                raise RuntimeError("Context capture is closed")
            self.sequence += 1
            call = Exchange(self, self.sequence)
            request = Body()
            request.observe(raw, self)
            self.write(
                "request",
                self.sequence,
                source="fixture" if provider == "fixture" else "provider",
                provider=provider,
                route=route,
                model=model,
                **request.record(),
            )
            self.pending[self.sequence] = call
            return call

    def close(self):
        with self.lock:
            for call in list(self.pending.values()):
                call.finish("interrupted")
            self.stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
