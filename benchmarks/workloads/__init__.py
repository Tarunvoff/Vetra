"""Benchmark workloads suite."""

from benchmarks.workloads.mixed import generate_mixed_workload
from benchmarks.workloads.multi_turn import generate_multi_turn_workload
from benchmarks.workloads.rag import generate_rag_workload
from benchmarks.workloads.repeated_prompt import generate_repeated_prompt_workload

__all__ = [
    "generate_multi_turn_workload",
    "generate_rag_workload",
    "generate_repeated_prompt_workload",
    "generate_mixed_workload",
]
