#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ -f "${REPO_ROOT}/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.env"
  set +a
fi

INFERENCE_POLICY="${INFERENCE_POLICY:-heuristic}"
API_TOKEN="${OPENAI_API_KEY:-${HF_TOKEN:-${HUGGINGFACEHUB_API_TOKEN:-${HF_API_TOKEN:-}}}}"
if [[ "$INFERENCE_POLICY" != "heuristic" && -z "${API_TOKEN}" ]]; then
  echo "Missing API token. Set one of: OPENAI_API_KEY, HF_TOKEN, HUGGINGFACEHUB_API_TOKEN, HF_API_TOKEN"
  echo "Hackathon path: use HF_TOKEN with OPENAI_BASE_URL=https://router.huggingface.co/v1"
  echo "Tip: create .env from .env.example and run this script again"
  exit 1
fi

if [[ -n "${API_TOKEN}" ]]; then
  export OPENAI_API_KEY="${API_TOKEN}"
fi
export OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://router.huggingface.co/v1}"

if [[ -z "${PYTHON_BIN:-}" ]]; then
  for candidate in "${REPO_ROOT}/.venv/bin/python" "$(cd "${REPO_ROOT}/.." && pwd)/.venv/bin/python"; do
    if [[ -x "${candidate}" ]]; then
      PYTHON_BIN="${candidate}"
      break
    fi
  done
fi

if [[ -z "${PYTHON_BIN:-}" || ! -x "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="$(command -v python3)"
fi

export PYTHONPATH="${REPO_ROOT}/src:${PYTHONPATH:-}"

mkdir -p "${REPO_ROOT}/outputs"
"$PYTHON_BIN" "${SCRIPT_DIR}/inference_round1.py" --seed 7 --policy "$INFERENCE_POLICY" --output "${REPO_ROOT}/outputs/round1_inference_report.json"
