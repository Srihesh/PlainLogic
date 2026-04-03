from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    classify_incident = "classify_incident"
    request_missing_fields = "request_missing_fields"
    assign_resource = "assign_resource"
    reroute_resource = "reroute_resource"
    escalate_to_regional = "escalate_to_regional"
    activate_shelter = "activate_shelter"
    defer_with_justification = "defer_with_justification"
    close_incident = "close_incident"


class Incident(BaseModel):
    incident_id: str
    severity: int = Field(ge=1, le=5)
    deadline_step: int = Field(ge=1)
    required_skill: str
    location: str
    requires_escalation: bool = False
    requires_shelter: bool = False
    status: str = "open"
    assigned_resource_id: Optional[str] = None
    classification: Optional[str] = None
    missing_fields_requested: bool = False
    shelter_activated: bool = False


class Resource(BaseModel):
    resource_id: str
    skill: str
    capacity: int = Field(ge=0)
    active_incident_id: Optional[str] = None


class Policy(BaseModel):
    max_steps: int = Field(ge=1)
    must_escalate_severity_5: bool = True
    max_open_high_severity: int = Field(ge=0)


class Metrics(BaseModel):
    valid_actions: int = 0
    invalid_actions: int = 0
    policy_violations: int = 0
    loops: int = 0
    incidents_closed: int = 0
    timely_closures: int = 0
    escalations_done: int = 0
    escalations_required: int = 0
    shelters_activated: int = 0
    shelters_required: int = 0


class Action(BaseModel):
    action_type: ActionType
    incident_id: Optional[str] = None
    resource_id: Optional[str] = None
    payload: Dict[str, str] = Field(default_factory=dict)


class Observation(BaseModel):
    task: str
    step: int
    remaining_steps: int
    incidents: List[Incident]
    resources: List[Resource]
    policy: Policy
    last_result: str


class EnvironmentState(BaseModel):
    task: str
    seed: int
    step: int = 0
    incidents: Dict[str, Incident]
    resources: Dict[str, Resource]
    policy: Policy
    metrics: Metrics = Field(default_factory=Metrics)
    done: bool = False
    action_fingerprint_history: List[str] = Field(default_factory=list)
    action_fingerprint_counts: Dict[str, int] = Field(default_factory=dict)
    last_result: str = "reset"


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    score: float
