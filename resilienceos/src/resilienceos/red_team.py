from __future__ import annotations

from resilienceos import Action, ActionType, ResilienceOSEnvironment
from resilienceos.baseline import choose_action


def run_invalid_payload_case() -> dict:
    env = ResilienceOSEnvironment()
    obs = env.reset(task="medium", seed=7)

    env.step(Action(action_type=ActionType.classify_incident, incident_id="I1", payload={}))

    done = False
    while not done:
        result = env.step(choose_action(task="medium", observation=obs))
        obs = result.observation
        done = result.done

    st = env.state()
    return {
        "scenario": "invalid_payload",
        "invalid_actions": st.metrics.invalid_actions,
        "policy_violations": st.metrics.policy_violations,
        "final_score": round(result.score, 6),
    }


def run_loop_case() -> dict:
    env = ResilienceOSEnvironment()
    obs = env.reset(task="hard", seed=7)

    env.step(Action(action_type=ActionType.activate_shelter, incident_id="I1"))
    env.step(Action(action_type=ActionType.activate_shelter, incident_id="I1"))

    done = False
    while not done:
        result = env.step(choose_action(task="hard", observation=obs))
        obs = result.observation
        done = result.done

    st = env.state()
    return {
        "scenario": "loop_repetition",
        "loops": st.metrics.loops,
        "invalid_actions": st.metrics.invalid_actions,
        "final_score": round(result.score, 6),
    }


def run_bad_resource_case() -> dict:
    env = ResilienceOSEnvironment()
    obs = env.reset(task="hard", seed=7)

    env.step(
        Action(
            action_type=ActionType.assign_resource,
            incident_id="I1",
            resource_id="R1",
        )
    )

    done = False
    while not done:
        result = env.step(choose_action(task="hard", observation=obs))
        obs = result.observation
        done = result.done

    st = env.state()
    return {
        "scenario": "bad_resource_assignment",
        "policy_violations": st.metrics.policy_violations,
        "invalid_actions": st.metrics.invalid_actions,
        "final_score": round(result.score, 6),
    }
