from kvguard.core.enums import SecurityAction
from kvguard.core.models import ACLRule, KVBlockStats
from kvguard.security.policy import SecurityPolicyEngine


def test_tenant_isolation_deny_cross_tenant(sample_block: KVBlockStats):
    sample_block.tenant_id = "tenant_alpha"
    engine = SecurityPolicyEngine()

    # Access by same tenant -> ALLOW
    decision_same = engine.authorize_access("tenant_alpha", sample_block)
    assert decision_same == SecurityAction.ALLOW

    # Access by different tenant -> DENY by default
    decision_diff = engine.authorize_access("tenant_beta", sample_block)
    assert decision_diff == SecurityAction.DENY


def test_tenant_acl_explicit_allow(sample_block: KVBlockStats):
    sample_block.tenant_id = "tenant_alpha"
    engine = SecurityPolicyEngine()
    engine.acl.add_rule(
        ACLRule(
            rule_id="rule_1",
            source_tenant_id="tenant_beta",
            target_tenant_id="tenant_alpha",
            target_namespace="*",
            action=SecurityAction.ALLOW,
        )
    )

    decision = engine.authorize_access("tenant_beta", sample_block)
    assert decision == SecurityAction.ALLOW
