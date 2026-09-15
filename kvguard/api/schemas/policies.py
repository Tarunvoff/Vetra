"""API Schemas for policy management."""

from pydantic import BaseModel
from kvguard.core.models import PolicyConstraints


class PolicyStatusResponse(BaseModel):
    engine_name: str
    active_policy: str = "rule_based"
    constraints: PolicyConstraints
    rules_count: int = 3
