"""Multi-turn conversation benchmark workload generator."""

import random
from typing import Any, Dict, List


def generate_multi_turn_workload(num_sessions: int = 5, turns_per_session: int = 4) -> List[Dict[str, Any]]:
    """Generate multi-turn conversation traces where subsequent turns reuse past session cache."""
    requests: List[Dict[str, Any]] = []

    for s_idx in range(num_sessions):
        session_id = f"session_conv_{s_idx:03d}"
        tenant_id = f"tenant_{s_idx % 2}"
        history_tokens = 64  # System prompt tokens

        for turn in range(turns_per_session):
            user_tokens = random.randint(30, 80)
            total_prompt_tokens = history_tokens + user_tokens
            cached_tokens = history_tokens if turn > 0 else 0  # Reuses prefix on turn > 0

            requests.append({
                "request_id": f"req_{session_id}_t{turn}",
                "session_id": session_id,
                "tenant_id": tenant_id,
                "turn": turn,
                "prompt_tokens": total_prompt_tokens,
                "cached_tokens": cached_tokens,
                "output_tokens": random.randint(40, 120),
            })
            history_tokens += user_tokens + 80  # Expand conversation history

    return requests
