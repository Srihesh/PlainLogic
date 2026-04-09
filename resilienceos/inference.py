from __future__ import annotations

import argparse
import json
import os
import re
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
BENCHMARK = os.getenv("MY_ENV_V4_BENCHMARK", "resilienceos")


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _format_bool(value: bool) -> str:
    return "true" if value else "false"


def _format_score(value: float) -> str:
    safe = min(0.999999, max(0.000001, value))
    return f"{safe:.6f}"


def _format_action(action: Action) -> str:
    incident_id = action.incident_id if action.incident_id is not None else "null"
    resource_id = action.resource_id if action.resource_id is not None else "null"
    payload = json.dumps(action.payload, ensure_ascii=True, separators=(",", ":"))
    return (
        f"{action.action_type.value}(incident_id={incident_id},"
        f"resource_id={resource_id},payload={payload})"
    )


def _error_from_last_result(last_result: str) -> str | None:
    if not last_result.startswith("invalid:"):
        return None
    message = last_result.split(":", 1)[1].strip()
    return re.sub(r"\s+", "_", message) or "invalid_action"


def _log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def _log_step(step: int, action: Action, reward: float, done: bool, error: str | None) -> None:
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={_format_action(action)} reward={reward:.2f} "
        f"done={_format_bool(done)} error={error_val}",
        flush=True,
    )


def _log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    reward_trace = rewards if rewards else [0.0]
    rewards_csv = ",".join(f"{r:.2f}" for r in reward_trace)
    print(
        f"[END] success={_format_bool(success)} steps={steps} score={_format_score(score)} rewards={rewards_csv}",
        flush=True,
    )


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


def _extract_json_object(raw_text: str) -> str:
    match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
    if not match:
        raise ValueError("no json object found in model response")
    return match.group(0)


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
    try:
        return _parse_action(content)
    except Exception:
        return _parse_action(_extract_json_object(content))


def _run_task(client: OpenAI | None, model: str, task: str, seed: int, policy: str) -> dict:
    env = ResilienceOSEnvironment()
    observation_obj = env.reset(task=task, seed=seed)
    observation = observation_obj.model_dump() if policy in {"model", "hybrid"} else None
    done = False
    steps = 0
    total_reward = 0.0
    final_score = 0.0
    rewards: list[float] = []
    task_error: Exception | None = None

    _log_start(task=task, env=BENCHMARK, model=model)

    try:
        while not done:
            if policy == "heuristic":
                action = choose_action(task=task, observation=observation_obj)
            elif policy == "model":
                if client is None:
                    raise RuntimeError("model policy requires API token")
                try:
                    if observation is None:
                        observation = observation_obj.model_dump()
                    action = _call_model(client=client, model=model, observation=observation)
                except Exception:
                    action = choose_action(task=task, observation=observation_obj)
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
            rewards.append(result.reward)
            final_score = result.score

            _log_step(
                step=steps,
                action=action,
                reward=result.reward,
                done=result.done,
                error=_error_from_last_result(result.observation.last_result),
            )
    except Exception as exc:
        task_error = exc
    finally:
        _log_end(success=task_error is None and done, steps=steps, score=final_score, rewards=rewards)

    if task_error is not None:
        raise task_error

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
        default=os.getenv("API_BASE_URL", "https://router.huggingface.co/v1"),
    )
    parser.add_argument(
        "--policy",
        type=str,
        choices=["heuristic", "model", "hybrid"],
        default="hybrid",
    )
    parser.add_argument("--output", type=str, default="outputs/round1_inference_report.json")
    args = parser.parse_args()

    api_key = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

    client = None
    if args.policy == "model":
        if not args.base_url:
            raise RuntimeError("Missing API_BASE_URL environment variable.")
        if not api_key:
            raise RuntimeError("Missing HF_TOKEN or API_KEY environment variable.")
        client = OpenAI(api_key=api_key, base_url=args.base_url, timeout=30)
    elif args.policy == "hybrid" and args.base_url and api_key:
        client = OpenAI(api_key=api_key, base_url=args.base_url, timeout=30)

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

if __name__ == "__main__":
    main()
