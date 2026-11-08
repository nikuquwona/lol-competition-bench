"""Verifier entry point. Invalid submissions get zero, including NaN and booleans."""

import json
import math
import os
import stat
from pathlib import Path

FIELDS = ("p_blue_win", "p_blue_ahead_15")


def score(prediction, labels):
    if not isinstance(prediction, dict) or set(prediction) != set(FIELDS):
        return 0.0
    errors = []
    for field in FIELDS:
        p = prediction[field]
        if type(p) not in (int, float) or not 0 <= p <= 1 or not math.isfinite(p):
            return 0.0
        errors.append((p - labels[field]) ** 2)
    return 1 - sum(errors) / len(errors)


def read_prediction(path):
    """Accept only a small regular file without following its final symlink."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 4096:
            raise ValueError("Invalid prediction file")
        content = os.read(fd, 4097)
        if len(content) > 4096:
            raise ValueError("Prediction exceeds size limit")
        return json.loads(content, object_pairs_hook=unique_fields)
    finally:
        os.close(fd)


def unique_fields(pairs):
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Duplicate JSON field")
    return result


if __name__ == "__main__":
    result = 0.0
    try:
        result = score(
            read_prediction("/app/prediction.json"),
            json.loads(Path("/tests/labels.json").read_bytes()),
        )
    except (ValueError, OSError, RecursionError):
        pass
    Path("/logs/verifier/reward.txt").write_text(str(result))
