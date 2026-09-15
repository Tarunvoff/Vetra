"""Simulated request generation modeling RAG, multi-turn, and prompt caching patterns."""

import random
import uuid
from typing import List
from kvguard.core.models import RequestStats


class SimulatedRequest:
    """Generates synthetic inference requests with predictable cache hit patterns."""

    @staticmethod
    def generate_batch(count: int = 10, hit_probability: float = 0.55) -> List[RequestStats]:
        requests: List[RequestStats] = []
        for i in range(count):
            req_id = f"req_{uuid.uuid4().hex[:8]}"
            tenant = f"tenant_{random.randint(0, 2)}"
            prompt_tokens = random.randint(128, 2048)
            is_hit = random.random() < hit_probability

            if is_hit:
                cached_tokens = int(prompt_tokens * random.uniform(0.4, 0.9))
                computed_tokens = prompt_tokens - cached_tokens
                ttft = random.uniform(40.0, 95.0)
            else:
                cached_tokens = 0
                computed_tokens = prompt_tokens
                ttft = random.uniform(140.0, 320.0)

            output_tokens = random.randint(32, 256)
            total_latency = ttft + (output_tokens * random.uniform(8.0, 14.0))

            requests.append(
                RequestStats(
                    request_id=req_id,
                    tenant_id=tenant,
                    session_id=f"session_{random.randint(1, 5)}",
                    prompt_tokens=prompt_tokens,
                    cached_tokens=cached_tokens,
                    computed_tokens=computed_tokens,
                    output_tokens=output_tokens,
                    ttft_ms=round(ttft, 2),
                    total_latency_ms=round(total_latency, 2),
                    cache_hit=is_hit,
                    hit_rate=round(cached_tokens / max(1, prompt_tokens), 3),
                )
            )
        return requests
