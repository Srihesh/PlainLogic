from __future__ import annotations

from .environment import ResilienceOSEnvironment
from .models import Action, ActionType


def choose_action(task: str, observation) -> Action:
    best_incident = None
    best_key = None
    for incident in observation.incidents:
        if incident.status == "closed":
            continue
        key = (-incident.severity, incident.deadline_step, incident.incident_id)
        if best_key is None or key < best_key:
            best_key = key
            best_incident = incident

    if best_incident is None:
        return Action(
            action_type=ActionType.defer_with_justification,
            incident_id=None,
            payload={"reason": "no-open-incidents"},
        )

    incidents = [best_incident]
    for incident in incidents:
        if incident.status == "closed":
            continue

        if incident.classification is None:
            label = "critical" if incident.severity >= 4 else "standard"
            return Action(
                action_type=ActionType.classify_incident,
                incident_id=incident.incident_id,
                payload={"label": label},
            )

        if incident.requires_escalation and not incident.escalation_completed:
            return Action(action_type=ActionType.escalate_to_regional, incident_id=incident.incident_id)

        if incident.requires_shelter and not incident.shelter_activated:
            return Action(action_type=ActionType.activate_shelter, incident_id=incident.incident_id)

        if incident.assigned_resource_id is None:
            for resource in observation.resources:
                if resource.skill == incident.required_skill and resource.capacity > 0:
                    return Action(
                        action_type=ActionType.assign_resource,
                        incident_id=incident.incident_id,
                        resource_id=resource.resource_id,
                    )

        if incident.assigned_resource_id is not None or incident.status == "escalated":
            return Action(action_type=ActionType.close_incident, incident_id=incident.incident_id)

    return Action(
        action_type=ActionType.defer_with_justification,
        incident_id=best_incident.incident_id,
        payload={"reason": "no-op fallback"},
    )


def run_task(task: str, seed: int) -> dict:
    env = ResilienceOSEnvironment()
    observation = env.reset(task=task, seed=seed)
    done = False
    final_score = 0.0
    steps = 0
    total_reward = 0.0

    while not done:
        action = choose_action(task=task, observation=observation)
        result = env.step(action)
        observation = result.observation
        done = result.done
        final_score = result.score
        total_reward += result.reward
        steps += 1

    return {
        "task": task,
        "seed": seed,
        "steps": steps,
        "total_reward": round(total_reward, 6),
        "final_score": round(final_score, 6),
    }
