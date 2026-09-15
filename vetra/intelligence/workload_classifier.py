"""Workload classification for pattern-tailored caching policies."""

from typing import List
from vetra.core.models import RequestStats


class WorkloadClassifier:
    """Classifies incoming inference traffic patterns."""

    @staticmethod
    def classify(requests: List[RequestStats]) -> str:
        """Classify workload as 'rag', 'multi_turn', 'repeated_prompt', or 'general'."""
        if not requests:
            return "general"

        avg_prompt_tokens = sum(r.prompt_tokens for r in requests) / len(requests)
        cached_ratio = sum(r.cached_tokens for r in requests) / max(1, sum(r.prompt_tokens for r in requests))

        if avg_prompt_tokens > 2000 and cached_ratio > 0.4:
            return "rag"
        elif any(r.session_id for r in requests):
            return "multi_turn"
        elif cached_ratio > 0.6:
            return "repeated_prompt"
        return "general"
