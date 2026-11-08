"""Verifier entry point. Invalid submissions get zero, including NaN and booleans."""

import json
import math
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


if __name__ == "__main__":
    prediction = Path("/app/prediction.json")
    result = 0.0
    try:
        if prediction.is_file() and prediction.stat().st_size <= 4096:
            result = score(
                json.loads(prediction.read_bytes()),
                json.loads(Path("/tests/labels.json").read_bytes()),
            )
    except (ValueError, OSError, RecursionError):
        pass
    Path("/logs/verifier/reward.txt").write_text(str(result))
