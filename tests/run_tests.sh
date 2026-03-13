#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v poetry >/dev/null 2>&1; then
  echo "[ERROR] Poetry n'est pas installe."
  exit 1
fi

# Ensure runtime + test dependencies required by conftest/app imports are present.
poetry run python - <<'PY'
import importlib.util
import subprocess
import sys

checks = {
    "pytest": "pytest",
    "pytest_cov": "pytest-cov",
    "httpx": "httpx",
    "sqlalchemy": "sqlalchemy",
    "fastapi": "fastapi",
    "passlib": "passlib[bcrypt]",
    "jose": "python-jose",
    "pydantic": "pydantic",
    "pydantic_settings": "pydantic-settings",
    "alembic": "alembic",
    "psycopg2": "psycopg2-binary",
}

missing = [pkg for module, pkg in checks.items() if importlib.util.find_spec(module) is None]
if missing:
    print("[INFO] Installation des dependances manquantes:", ", ".join(missing))
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
else:
    print("[INFO] Dependances de test deja disponibles.")
PY

if [[ "${1:-}" == "--deps-only" ]]; then
  echo "[INFO] Verification des dependances terminee."
  exit 0
fi

MODE="normal"
if [[ "${1:-}" == "--cov" ]]; then
  MODE="cov"
  shift
fi

# If no explicit test target is provided, run the whole tests folder.
if [[ "$#" -eq 0 ]]; then
  set -- tests
fi

if [[ "$MODE" == "cov" ]]; then
  poetry run pytest "$@" --cov=app --cov-report=term-missing --cov-report=html
else
  poetry run pytest "$@"
fi
