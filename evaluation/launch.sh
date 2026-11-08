# The bench trampoline also supports an explicit invocation with python3.12 bench.
set -eu

run_if_supported() {
    if "$1" -I -c 'import sys; sys.exit(sys.version_info < (3, 12))' >/dev/null 2>&1; then
        exec "$@"
    fi
}

if [ -n "${VIRTUAL_ENV:-}" ]; then
    run_if_supported "$VIRTUAL_ENV/bin/python" "$@"
fi
run_if_supported "$(dirname "$1")/.venv/bin/python" "$@"
for candidate in python3 python3.12 python3.13 python3.14 python3.15; do
    run_if_supported "$candidate" "$@"
done
if candidate=$(uv --offline --no-cache python find --no-python-downloads '>=3.12' 2>/dev/null); then
    run_if_supported "$candidate" "$@"
fi
echo 'LoL Competition Bench requires a working Python 3.12+. Install one or activate a compatible virtual environment.' >&2
exit 1
