"""Composite realistic mixed benchmark workload generator."""

import random
from typing import Any, Dict, List
from benchmarks.workloads.multi_turn import generate_multi_turn_workload
from benchmarks.workloads.rag import generate_rag_workload
from benchmarks.workloads.repeated_prompt import generate_repeated_prompt_workload


def generate_mixed_workload(seed: int = 42) -> List[Dict[str, Any]]:
    """Generate a combined, shuffled distribution of multi-turn, RAG, and repeated prompts."""
    random.seed(seed)
    reqs: List[Dict[str, Any]] = []

    reqs.extend(generate_multi_turn_workload(num_sessions=3, turns_per_session=3))
    reqs.extend(generate_rag_workload(num_docs=2, questions_per_doc=4))
    reqs.extend(generate_repeated_prompt_workload(num_requests=10))

    random.shuffle(reqs)
    return reqs
