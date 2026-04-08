from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from resilienceos import Action, ActionType, ResilienceOSEnvironment  # noqa: E402
from resilienceos.baseline import choose_action  # noqa: E402

SYSTEM_PROMPT = (
    "You are an operations planner. Return exactly one JSON object with keys "
    "action_type, incident_id, resource_id, payload. No extra text."
)
TASKS = ["easy", "medium", "hard"]


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _emit(tag: str, payload: dict) -> None:
    print(f"{tag} {json.dumps(payload, ensure_ascii=True, separators=(',', ':'))}")


def _build_user_prompt(observation: dict) -> str:
    return json.dumps({"observation": observation}, ensure_ascii=True)


def _parse_action(raw_text: str) -> Action:
    payload = json.loads(raw_text)
    raw_action_type = str(payload.get("action_type", "")).strip().lower()
    normalized = {
        "assign_resource_to_incident": "assign_resource",
        "assign_to_incident": "assign_resource",
        "assign": "assign_resource",
        "close": "close_incident",
        "escalate": "escalate_to_regional",
        "request_missing": "request_missing_fields",
        "request_missing_info": "request_missing_fields",
        "activate_shelter_for_incident": "activate_shelter",
        "defer": "defer_with_justification",
        "classify": "classify_incident",
    }.get(raw_action_type, raw_action_type)
    return Action(
        action_type=ActionType(normalized),
        incident_id=payload.get("incident_id"),
        resource_id=payload.get("resource_id"),
        payload=payload.get("payload", {}),
    )


def _call_model(client: OpenAI, model: str, observation: dict) -> Action:
    completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(observation)},
        ],
    )
    content = completion.choices[0].message.content or "{}"
    return _parse_action(content)


def _run_task(client: OpenAI | None, model: str, task: str, seed: int, policy: str) -> dict:
    env = ResilienceOSEnvironment()
    observation_obj = env.reset(task=task, seed=seed)
    observation = observation_obj.model_dump() if policy in {"model", "hybrid"} else None
    done = False
    steps = 0
    total_reward = 0.0
    final_score = 0.0

    while not done:
        if policy == "heuristic":
            action = choose_action(task=task, observation=observation_obj)
        elif policy == "model":
            if client is None:
                raise RuntimeError("model policy requires API token")
            if observation is None:
                observation = observation_obj.model_dump()
            action = _call_model(client=client, model=model, observation=observation)
        else:
            try:
                if client is None:
                    raise RuntimeError("missing API client")
                if observation is None:
                    observation = observation_obj.model_dump()
                action = _call_model(client=client, model=model, observation=observation)
            except Exception:
                action = choose_action(task=task, observation=observation_obj)

        result = env.step(action)
        observation_obj = result.observation
        if policy in {"model", "hybrid"}:
            observation = observation_obj.model_dump()
        done = result.done
        steps += 1
        total_reward += result.reward
        final_score = result.score

        _emit(
            "[STEP]",
            {
                "ts": _ts(),
                "task": task,
                "step": steps,
                "action_type": action.action_type.value,
                "incident_id": action.incident_id,
                "resource_id": action.resource_id,
                "reward": round(result.reward, 6),
                "score": round(result.score, 6),
                "done": result.done,
                "last_result": result.observation.last_result,
            },
        )

    return {
        "task": task,
        "seed": seed,
        "steps": steps,
        "total_reward": round(total_reward, 6),
        "final_score": round(final_score, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--model", type=str, default=os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct"))
    parser.add_argument(
        "--base-url",
        type=str,
        default=(
            os.getenv("API_BASE_URL")
            or os.getenv("OPENAI_BASE_URL")
            or "https://router.huggingface.co/v1"
        ),
    )
    parser.add_argument(
        "--policy",
        type=str,
        choices=["heuristic", "model", "hybrid"],
        default=os.getenv("INFERENCE_POLICY", "heuristic"),
    )
    parser.add_argument("--output", type=str, default="outputs/round1_inference_report.json")
    args = parser.parse_args()

    api_key = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("HF_TOKEN")
        or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        or os.getenv("HF_API_TOKEN")
    )

    _emit(
        "[START]",
        {
            "ts": _ts(),
            "env": "resilienceos",
            "seed": args.seed,
            "model": args.model,
            "base_url": args.base_url,
            "policy": args.policy,
            "tasks": TASKS,
        },
    )

    client = None
    if args.policy in {"model", "hybrid"}:
        if not api_key:
            _emit(
                "[END]",
                {
                    "ts": _ts(),
                    "status": "error",
                    "error": "Missing API token. Set OPENAI_API_KEY or HF_TOKEN.",
                },
            )
            raise RuntimeError(
                "Missing API token. Set OPENAI_API_KEY or HF_TOKEN. "
                "For hackathon free credits, prefer HF_TOKEN with API_BASE_URL=https://router.huggingface.co/v1"
            )
        client = OpenAI(api_key=api_key, base_url=args.base_url)

    task_reports = [_run_task(client=client, model=args.model, task=t, seed=args.seed, policy=args.policy) for t in TASKS]
    aggregate = sum(r["final_score"] for r in task_reports) / len(task_reports)

    report = {
        "env": "resilienceos",
        "generated_at": _ts(),
        "seed": args.seed,
        "model": args.model,
        "base_url": args.base_url,
        "policy": args.policy,
        "tasks": task_reports,
        "aggregate_score": round(aggregate, 6),
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    _emit(
        "[END]",
        {
            "ts": _ts(),
            "env": report["env"],
            "seed": report["seed"],
            "policy": report["policy"],
            "aggregate_score": report["aggregate_score"],
            "output": str(output_path),
            "status": "ok",
        },
    )


if __name__ == "__main__":
    main()
