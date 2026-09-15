"""Retrieval-Augmented Generation (RAG) benchmark workload generator."""

import random
from typing import Any, Dict, List


def generate_rag_workload(num_docs: int = 4, questions_per_doc: int = 5) -> List[Dict[str, Any]]:
    """Generate RAG traces where multiple queries reference the same retrieved document chunks."""
    requests: List[Dict[str, Any]] = []

    for d_idx in range(num_docs):
        doc_id = f"doc_{d_idx:02d}"
        doc_tokens = random.randint(1500, 3000)
        sys_tokens = 50

        for q_idx in range(questions_per_doc):
            query_tokens = random.randint(20, 50)
            total_prompt = sys_tokens + doc_tokens + query_tokens
            # Document prefix is cached on repeated questions to the same doc
            cached_tokens = (sys_tokens + doc_tokens) if q_idx > 0 else 0

            requests.append({
                "request_id": f"req_rag_{doc_id}_q{q_idx}",
                "session_id": f"rag_{doc_id}",
                "tenant_id": f"tenant_{d_idx % 2}",
                "doc_id": doc_id,
                "prompt_tokens": total_prompt,
                "cached_tokens": cached_tokens,
                "output_tokens": random.randint(80, 200),
            })

    return requests
