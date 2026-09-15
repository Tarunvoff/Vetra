"""Repeated system prompt prefix benchmark workload generator."""

import random
from typing import Any, Dict, List


def generate_repeated_prompt_workload(
    num_requests: int = 20, prefix_tokens: int = 512
) -> List[Dict[str, Any]]:
    """Generate traffic sharing a single static system instruction prefix."""
    requests: List[Dict[str, Any]] = []

    for i in range(num_requests):
        unique_tokens = random.randint(20, 100)
        total_prompt = prefix_tokens + unique_tokens
        cached_tokens = prefix_tokens if i > 0 else 0

        requests.append({
            "request_id": f"req_sys_rep_{i:03d}",
            "session_id": "shared_system_prompt",
            "tenant_id": "default",
            "prompt_tokens": total_prompt,
            "cached_tokens": cached_tokens,
            "output_tokens": random.randint(30, 90),
        })

    return requests
