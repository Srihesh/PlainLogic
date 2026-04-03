from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INFER_SCRIPT = ROOT / "scripts" / "inference_round1.py"
OUTPUT_DIR = ROOT / "outputs"


def run_policy(policy: str) -> dict:
    output_path = OUTPUT_DIR / f"round1_inference_report_{policy}.json"
    cmd = [
        sys.executable,
        str(INFER_SCRIPT),
        "--seed",
        "7",
        "--policy",
        policy,
        "--output",
        str(output_path),
    ]

    try:
        subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
        data = json.loads(output_path.read_text(encoding="utf-8"))
        return {
            "policy": policy,
            "status": "pass",
            "aggregate_score": data.get("aggregate_score"),
            "tasks": data.get("tasks", []),
            "output": output_path.name,
        }
    except subprocess.CalledProcessError as exc:
        return {
            "policy": policy,
            "status": "fail",
            "error": (exc.stderr or exc.stdout or "unknown error")[-600:],
        }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    have_token = any(
        os.getenv(k)
        for k in ["OPENAI_API_KEY", "HF_TOKEN", "HUGGINGFACEHUB_API_TOKEN", "HF_API_TOKEN"]
    )

    policies = ["heuristic"]
    if have_token:
        policies.extend(["hybrid", "model"])

    results = [run_policy(p) for p in policies]
    report = {
        "seed": 7,
        "token_present": have_token,
        "results": results,
    }

    report_path = OUTPUT_DIR / "eval_matrix_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
