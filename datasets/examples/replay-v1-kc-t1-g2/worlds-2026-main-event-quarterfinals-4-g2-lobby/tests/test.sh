#!/bin/sh
set -eu
mkdir -p /logs/verifier
python3 -I /tests/score.py
