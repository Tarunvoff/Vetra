"""Custom rule declarations and rule registry."""

from typing import Callable, List, Optional
from vetra.core.enums import DecisionType
from vetra.core.models import GPUStats, KVBlockStats, Recommendation
from vetra.policy.recommendation import build_recommendation

RuleFunction = Callable[[KVBlockStats, GPUStats, float], Optional[Recommendation]]


class RuleRegistry:
    """Registry for pluggable policy rules."""

    def __init__(self) -> None:
        self._rules: List[RuleFunction] = []

    def register(self, rule_fn: RuleFunction) -> None:
        self._rules.append(rule_fn)

    def evaluate_rules(
        self, block: KVBlockStats, gpu_stats: GPUStats, importance: float
    ) -> Optional[Recommendation]:
        for rule in self._rules:
            res = rule(block, gpu_stats, importance)
            if res is not None:
                return res
        return None
