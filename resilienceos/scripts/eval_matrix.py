from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parent.parent
INFER_SCRIPT = ROOT / "scripts" / "inference_round1.py"
OUTPUT_DIR = ROOT / "outputs"


def _parse_seeds() -> list[int]:
    raw = os.getenv("EVAL_SEEDS", "7,12,19")
    seeds: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if part:
            seeds.append(int(part))
    return seeds or [7]


def _summarize_runs(policy: str, runs: list[dict]) -> dict:
    aggregate_scores = [run["aggregate_score"] for run in runs]
    task_names = sorted({task["task"] for run in runs for task in run["tasks"]})
    per_task = []
    for task_name in task_names:
        task_scores = [
            task["final_score"]
            for run in runs
            for task in run["tasks"]
            if task["task"] == task_name
        ]
        per_task.append(
            {
                "task": task_name,
                "avg_final_score": round(mean(task_scores), 6),
                "min_final_score": round(min(task_scores), 6),
                "max_final_score": round(max(task_scores), 6),
            }
        )

    return {
        "policy": policy,
        "status": "pass",
        "seeds": [run["seed"] for run in runs],
        "avg_aggregate_score": round(mean(aggregate_scores), 6),
        "min_aggregate_score": round(min(aggregate_scores), 6),
        "max_aggregate_score": round(max(aggregate_scores), 6),
        "per_task": per_task,
        "runs": runs,
    }


def run_policy(policy: str, seeds: list[int]) -> dict:
    runs: list[dict] = []
    output_files: list[str] = []

    for seed in seeds:
        output_path = OUTPUT_DIR / f"round1_inference_report_{policy}_seed{seed}.json"
        cmd = [
            sys.executable,
            str(INFER_SCRIPT),
            "--seed",
            str(seed),
            "--policy",
            policy,
            "--output",
            str(output_path),
        ]

        try:
            subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
            data = json.loads(output_path.read_text(encoding="utf-8"))
        except subprocess.CalledProcessError as exc:
            return {
                "policy": policy,
                "status": "fail",
                "seed": seed,
                "error": (exc.stderr or exc.stdout or "unknown error")[-600:],
            }

        runs.append(
            {
                "seed": seed,
                "aggregate_score": data.get("aggregate_score"),
                "tasks": data.get("tasks", []),
                "output": output_path.name,
            }
        )
        output_files.append(output_path.name)

    summary = _summarize_runs(policy=policy, runs=runs)
    summary["output_files"] = output_files
    return summary


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    seeds = _parse_seeds()
    have_token = any(
        os.getenv(k)
        for k in ["OPENAI_API_KEY", "HF_TOKEN", "HUGGINGFACEHUB_API_TOKEN", "HF_API_TOKEN"]
    )

    policies = ["heuristic"]
    if have_token:
        policies.extend(["hybrid", "model"])

    results = [run_policy(p, seeds=seeds) for p in policies]
    report = {
        "seeds": seeds,
        "token_present": have_token,
        "results": results,
    }

    report_path = OUTPUT_DIR / "eval_matrix_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
