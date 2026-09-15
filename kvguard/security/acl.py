"""Access Control List (ACL) registry and rule evaluation."""

from typing import Dict, List, Optional
from kvguard.core.enums import SecurityAction
from kvguard.core.models import ACLRule


class ACLRegistry:
    """Stores cross-tenant sharing rules."""

    def __init__(self) -> None:
        self._rules: Dict[str, ACLRule] = {}

    def add_rule(self, rule: ACLRule) -> None:
        self._rules[rule.rule_id] = rule

    def check_permission(
        self, source_tenant: str, target_tenant: str, target_namespace: str = "default"
    ) -> SecurityAction:
        """Check if source_tenant is allowed to access target_tenant's cache."""
        # Own tenant always allowed
        if source_tenant == target_tenant:
            return SecurityAction.ALLOW

        # Check explicit sharing rules
        for rule in self._rules.values():
            if (
                rule.source_tenant_id == source_tenant
                and rule.target_tenant_id == target_tenant
                and (rule.target_namespace == "*" or rule.target_namespace == target_namespace)
            ):
                return rule.action

        return SecurityAction.DENY
