"""Security policy engine enforcing tenant boundaries and access rules."""

import uuid
from kvguard.core.enums import SecurityAction
from kvguard.core.interfaces import ISecurityPolicyEngine
from kvguard.core.models import KVBlockStats, SecurityEvent
from kvguard.security.acl import ACLRegistry
from kvguard.security.audit import SecurityAuditLogger
from kvguard.security.isolation import TenantIsolationValidator
from kvguard.security.ttl import TTLManager


class SecurityPolicyEngine(ISecurityPolicyEngine):
    """Central security evaluation controller."""

    def __init__(
        self,
        acl_registry: ACLRegistry | None = None,
        audit_logger: SecurityAuditLogger | None = None,
    ) -> None:
        self.acl = acl_registry or ACLRegistry()
        self.validator = TenantIsolationValidator(self.acl)
        self.audit = audit_logger or SecurityAuditLogger()

    def authorize_access(
        self,
        requesting_tenant: str,
        target_block: KVBlockStats,
        operation: str = "read",
    ) -> SecurityAction:
        # Check TTL first
        if not TTLManager.is_block_valid(target_block):
            decision = SecurityAction.DENY
            reason = f"Block {target_block.block_id} TTL expired."
        else:
            decision = self.validator.validate_access(requesting_tenant, target_block)
            reason = (
                f"Access granted: tenant match or ACL allow."
                if decision == SecurityAction.ALLOW
                else f"Access denied: cross-tenant isolation ({requesting_tenant} -> {target_block.tenant_id})."
            )

        event = SecurityEvent(
            event_id=str(uuid.uuid4())[:8],
            source_tenant_id=requesting_tenant,
            target_block_id=target_block.block_id,
            action_attempted=operation,
            decision=decision,
            reason=reason,
        )
        self.audit.record_event(event)
        return decision
