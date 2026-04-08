from __future__ import annotations

from typing import Optional

from .fixtures import build_incidents, build_policy, build_resources
from .grading import compute_final_score, compute_step_reward
from .models import Action, ActionType, EnvironmentState, Observation, StepResult


class ResilienceOSEnvironment:
    def __init__(self) -> None:
        self._state: Optional[EnvironmentState] = None

    def reset(self, task: str = "easy", seed: int = 0) -> Observation:
        task = task.lower()
        if task not in {"easy", "medium", "hard"}:
            raise ValueError("task must be one of: easy, medium, hard")
        incidents = build_incidents(task=task, seed=seed)
        resources = build_resources(task=task, seed=seed)
        policy = build_policy(task=task)
        escalations_required = sum(1 for i in incidents.values() if i.requires_escalation)
        shelters_required = sum(1 for i in incidents.values() if i.requires_shelter)

        self._state = EnvironmentState(
            task=task,
            seed=seed,
            incidents=incidents,
            resources=resources,
            policy=policy,
        )
        self._state.metrics.escalations_required = escalations_required
        self._state.metrics.shelters_required = shelters_required
        self._state.last_result = "reset_ok"
        return self._observation()

    def step(self, action: Action) -> StepResult:
        state = self._require_state()
        if state.done:
            return StepResult(
                observation=self._observation(),
                reward=0.0,
                done=True,
                score=compute_final_score(state),
            )

        state.step += 1
        fingerprint = f"{action.action_type.value}:{action.incident_id}:{action.resource_id}:{sorted(action.payload.items())}"
        state.action_fingerprint_history.append(fingerprint)
        state.action_fingerprint_counts[fingerprint] = state.action_fingerprint_counts.get(fingerprint, 0) + 1
        if state.action_fingerprint_counts[fingerprint] > 1:
            state.metrics.loops += 1

        was_valid, progress_gain = self._apply_action(action)
        reward = compute_step_reward(state=state, was_valid=was_valid, progress_gain=progress_gain)

        if state.step >= state.policy.max_steps:
            state.done = True
            state.last_result = "max_steps_reached"

        if all(i.status == "closed" for i in state.incidents.values()):
            state.done = True
            state.last_result = "all_incidents_closed"

        score = compute_final_score(state)
        return StepResult(observation=self._observation(), reward=reward, done=state.done, score=score)

    def state(self) -> EnvironmentState:
        return self._require_state()

    def _require_state(self) -> EnvironmentState:
        if self._state is None:
            raise RuntimeError("Environment not initialized. Call reset first.")
        return self._state

    def _observation(self) -> Observation:
        state = self._require_state()
        return Observation(
            task=state.task,
            step=state.step,
            remaining_steps=max(0, state.policy.max_steps - state.step),
            incidents=list(state.incidents.values()),
            resources=list(state.resources.values()),
            policy=state.policy,
            last_result=state.last_result,
        )

    def _apply_action(self, action: Action) -> tuple[bool, float]:
        state = self._require_state()
        incident = state.incidents.get(action.incident_id or "") if action.incident_id else None
        resource = state.resources.get(action.resource_id or "") if action.resource_id else None

        if action.action_type == ActionType.request_missing_fields:
            if incident is None:
                return self._invalid("missing incident for request_missing_fields")
            incident.missing_fields_requested = True
            state.metrics.valid_actions += 1
            state.last_result = "missing_fields_requested"
            return True, 0.03

        if action.action_type == ActionType.classify_incident:
            if incident is None:
                return self._invalid("missing incident for classify_incident")
            label = action.payload.get("label")
            if not label:
                return self._invalid("missing label payload")
            incident.classification = label
            state.metrics.valid_actions += 1
            state.last_result = "classified"
            return True, 0.07

        if action.action_type in {ActionType.assign_resource, ActionType.reroute_resource}:
            if incident is None or resource is None:
                return self._invalid("missing incident or resource for assignment")
            if incident.status == "closed":
                return self._invalid("cannot assign closed incident")
            if resource.capacity <= 0 and resource.active_incident_id != incident.incident_id:
                return self._invalid("resource unavailable")
            if incident.classification is None:
                state.metrics.policy_violations += 1
            if resource.skill != incident.required_skill:
                state.metrics.policy_violations += 1
            if resource.active_incident_id and resource.active_incident_id != incident.incident_id:
                previous = state.incidents.get(resource.active_incident_id)
                if previous is not None and previous.status != "closed":
                    previous.status = "open"
            resource.active_incident_id = incident.incident_id
            resource.capacity = 0
            incident.assigned_resource_id = resource.resource_id
            incident.status = "in_progress"
            state.metrics.valid_actions += 1
            state.last_result = "resource_assigned"
            return True, 0.12

        if action.action_type == ActionType.escalate_to_regional:
            if incident is None:
                return self._invalid("missing incident for escalate")
            if incident.status == "closed":
                return self._invalid("cannot escalate closed incident")
            if incident.escalation_completed:
                state.metrics.loops += 1
                state.last_result = "incident_already_escalated"
                return True, 0.0
            incident.escalation_completed = True
            incident.status = "escalated"
            state.metrics.escalations_done += 1
            state.metrics.valid_actions += 1
            state.last_result = "escalated"
            return True, 0.10

        if action.action_type == ActionType.activate_shelter:
            if incident is None:
                return self._invalid("missing incident for shelter")
            if not incident.requires_shelter:
                state.metrics.policy_violations += 1
            if incident.shelter_activated:
                state.metrics.loops += 1
                state.last_result = "shelter_already_active"
                return True, 0.0
            incident.shelter_activated = True
            state.metrics.shelters_activated += 1
            state.metrics.valid_actions += 1
            state.last_result = "shelter_activated"
            return True, 0.08

        if action.action_type == ActionType.defer_with_justification:
            if incident is None:
                return self._invalid("missing incident for defer")
            justification = action.payload.get("reason", "").strip()
            if not justification:
                return self._invalid("missing defer justification")
            incident.status = "deferred"
            if incident.severity >= 4:
                state.metrics.policy_violations += 1
            state.metrics.valid_actions += 1
            state.last_result = "deferred"
            return True, 0.01

        if action.action_type == ActionType.close_incident:
            if incident is None:
                return self._invalid("missing incident for close")
            was_escalated_before_close = incident.escalation_completed
            if incident.status not in {"in_progress", "escalated"}:
                state.metrics.policy_violations += 1
            if incident.classification is None:
                state.metrics.policy_violations += 1
            if incident.requires_shelter and not incident.shelter_activated:
                state.metrics.policy_violations += 1
            if not incident.assigned_resource_id and not was_escalated_before_close:
                state.metrics.policy_violations += 1
            incident.status = "closed"
            state.metrics.incidents_closed += 1
            if state.step <= incident.deadline_step:
                state.metrics.timely_closures += 1
            if incident.assigned_resource_id:
                resource = state.resources.get(incident.assigned_resource_id)
                if resource:
                    resource.capacity = 1
                    resource.active_incident_id = None
            if incident.requires_escalation and not was_escalated_before_close:
                state.metrics.policy_violations += 1
            state.metrics.valid_actions += 1
            state.last_result = "closed"
            return True, 0.20

        return self._invalid("unsupported action")

    def _invalid(self, reason: str) -> tuple[bool, float]:
        state = self._require_state()
        state.metrics.invalid_actions += 1
        state.last_result = f"invalid:{reason}"
        return False, 0.0
