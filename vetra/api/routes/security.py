"""Security, tenant isolation, and audit trail endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from vetra.api.dependencies import ServiceContainer, get_container
from vetra.core.models import SecurityEvent

router = APIRouter(prefix="/security", tags=["Security"])


@router.get("/status")
async def get_security_status(
    container: ServiceContainer = Depends(get_container),
) -> Dict[str, Any]:
    return {
        "security_enabled": container.settings.features.enable_security,
        "phase": "Phase 2 (Architectural Interface & ACL Registry)",
        "isolation_mode": "strict_tenant_boundary",
        "registered_rules": len(container.security_engine.acl._rules),
    }


@router.get("/audit")
async def get_security_audit_trail(
    limit: int = 50,
    container: ServiceContainer = Depends(get_container),
) -> List[Any]:
    events = container.security_engine.audit.list_events(limit=limit)
    return [e.model_dump() if hasattr(e, "model_dump") else e for e in events]
