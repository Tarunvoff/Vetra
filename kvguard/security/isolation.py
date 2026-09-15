"""Tenant isolation boundary enforcement."""

from kvguard.core.enums import SecurityAction
from kvguard.core.models import KVBlockStats
from kvguard.security.acl import ACLRegistry


class TenantIsolationValidator:
    """Enforces zero cross-tenant cache contamination."""

    def __init__(self, acl_registry: ACLRegistry | None = None) -> None:
        self.acl = acl_registry or ACLRegistry()

    def validate_access(self, requesting_tenant: str, target_block: KVBlockStats) -> SecurityAction:
        if requesting_tenant == target_block.tenant_id:
            return SecurityAction.ALLOW

        # Fallback to ACL registry
        return self.acl.check_permission(
            source_tenant=requesting_tenant,
            target_tenant=target_block.tenant_id,
        )
