from __future__ import annotations

from typing import Dict

from .models import Incident, Policy, Resource

def build_policy(task: str) -> Policy:
    if task == "easy":
        return Policy(max_steps=8, must_escalate_severity_5=True, max_open_high_severity=1)
    if task == "medium":
        return Policy(max_steps=14, must_escalate_severity_5=True, max_open_high_severity=2)
    return Policy(max_steps=20, must_escalate_severity_5=True, max_open_high_severity=2)


def build_incidents(task: str, seed: int) -> Dict[str, Incident]:
    if task == "easy":
        return {
            "I1": Incident(
                incident_id="I1",
                severity=3,
                deadline_step=5,
                required_skill="medical",
                location=f"zone-{(seed + 1) % 3}",
                requires_escalation=False,
                requires_shelter=False,
            )
        }
    if task == "medium":
        fire_deadline = 6 + (seed % 2)
        medical_deadline = 8 + ((seed + 1) % 2)
        hazmat_deadline = 5 + (seed % 2)
        return {
            "I1": Incident(
                incident_id="I1",
                severity=4,
                deadline_step=fire_deadline,
                required_skill="fire",
                location=f"zone-{(seed + 2) % 4}",
                requires_escalation=False,
                requires_shelter=False,
            ),
            "I2": Incident(
                incident_id="I2",
                severity=2,
                deadline_step=medical_deadline,
                required_skill="medical",
                location=f"zone-{(seed + 3) % 4}",
                requires_escalation=False,
                requires_shelter=True,
            ),
            "I3": Incident(
                incident_id="I3",
                severity=5,
                deadline_step=hazmat_deadline,
                required_skill="hazmat",
                location=f"zone-{(seed + 1) % 4}",
                requires_escalation=True,
                requires_shelter=False,
            ),
        }
    fire_deadline = 5 + (seed % 2)
    medical_deadline = 7 + ((seed + 1) % 2)
    logistics_deadline = 8 + ((seed + 2) % 2)
    hazmat_deadline = 6 + ((seed + 1) % 2)
    return {
        "I1": Incident(
            incident_id="I1",
            severity=5,
            deadline_step=fire_deadline,
            required_skill="fire",
            location=f"zone-{(seed + 1) % 5}",
            requires_escalation=True,
            requires_shelter=True,
        ),
        "I2": Incident(
            incident_id="I2",
            severity=4,
            deadline_step=medical_deadline,
            required_skill="medical",
            location=f"zone-{(seed + 2) % 5}",
            requires_escalation=False,
            requires_shelter=False,
        ),
        "I3": Incident(
            incident_id="I3",
            severity=3,
            deadline_step=logistics_deadline,
            required_skill="logistics",
            location=f"zone-{(seed + 3) % 5}",
            requires_escalation=False,
            requires_shelter=True,
        ),
        "I4": Incident(
            incident_id="I4",
            severity=5,
            deadline_step=hazmat_deadline,
            required_skill="hazmat",
            location=f"zone-{(seed + 4) % 5}",
            requires_escalation=True,
            requires_shelter=False,
        ),
    }


def build_resources(task: str, seed: int) -> Dict[str, Resource]:
    base = {
        "R1": Resource(resource_id="R1", skill="medical", capacity=1),
        "R2": Resource(resource_id="R2", skill="fire", capacity=1),
        "R3": Resource(resource_id="R3", skill="hazmat", capacity=1),
    }
    if task == "easy":
        return {
            "R1": Resource(resource_id="R1", skill="medical", capacity=1),
            "R4": Resource(resource_id=f"R4-{seed % 2}", skill="medical", capacity=1),
        }
    if task == "medium":
        return base
    return {
        **base,
        "R4": Resource(resource_id="R4", skill="logistics", capacity=1),
    }
