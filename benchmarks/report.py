"""Benchmark comparison report generator (Terminal Table, JSON, CSV, and Markdown)."""

import asyncio
import csv
import json
import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console
from rich.table import Table
from benchmarks.runners.baseline import run_baseline_benchmark
from benchmarks.runners.kvguard import run_kvguard_benchmark


def generate_markdown_report(baseline, kvguard) -> str:
    hit_delta = f"{(kvguard.cache_hit_rate - baseline.cache_hit_rate) * 100.0:+.1f}%"
    kv_delta = f"{((kvguard.kv_memory_gb - baseline.kv_memory_gb) / baseline.kv_memory_gb) * 100.0:+.1f}%"
    ttft_delta = f"{((kvguard.avg_ttft_ms - baseline.avg_ttft_ms) / baseline.avg_ttft_ms) * 100.0:+.1f}%"
    gpu_delta = f"{((kvguard.gpu_memory_gb - baseline.gpu_memory_gb) / baseline.gpu_memory_gb) * 100.0:+.1f}%"
    cost_delta = f"{((kvguard.estimated_cost_per_hour_usd - baseline.estimated_cost_per_hour_usd) / baseline.estimated_cost_per_hour_usd) * 100.0:+.1f}%"

    md = f"""# KVGuard Benchmark Evaluation Report

**Workload**: `{kvguard.workload}` | **Requests**: `{kvguard.total_requests}` | **Status**: `{'SIMULATION' if kvguard.is_simulation else 'LIVE'}`

| Metric | Baseline | KVGuard | Delta |
| :--- | :--- | :--- | :--- |
| **Cache Hit Rate** | {baseline.cache_hit_rate * 100.0:.1f}% | {kvguard.cache_hit_rate * 100.0:.1f}% | **{hit_delta}** |
| **KV Memory** | {baseline.kv_memory_gb:.1f} GB | {kvguard.kv_memory_gb:.1f} GB | **{kv_delta}** |
| **TTFT** | {baseline.avg_ttft_ms:.0f} ms | {kvguard.avg_ttft_ms:.0f} ms | **{ttft_delta}** |
| **GPU Memory** | {baseline.gpu_memory_gb:.1f} GB | {kvguard.gpu_memory_gb:.1f} GB | **{gpu_delta}** |
| **Estimated Cost** | ${baseline.estimated_cost_per_hour_usd:.2f}/hr | ${kvguard.estimated_cost_per_hour_usd:.2f}/hr | **{cost_delta}** |
| **Memory Saved** | — | {kvguard.memory_saved_gb:.1f} GB | **+{kvguard.memory_saved_gb:.1f} GB** |
"""
    return md


async def run_and_print_report(format_type: str = "table"):
    console = Console()
    baseline = await run_baseline_benchmark(workload_type="mixed", num_requests=50)
    kvguard = await run_kvguard_benchmark(workload_type="mixed", num_requests=50)

    if format_type == "json":
        data = {
            "baseline": baseline.model_dump(),
            "kvguard": kvguard.model_dump(),
        }
        print(json.dumps(data, indent=2))
        return

    if format_type == "markdown":
        print(generate_markdown_report(baseline, kvguard))
        return

    # Rich Table output
    table = Table(title="KVGuard Benchmark Evaluation: Baseline vs KVGuard (SIMULATION)")
    table.add_column("Metric", style="cyan")
    table.add_column("Baseline", justify="right")
    table.add_column("KVGuard", justify="right", style="bold green")
    table.add_column("Delta", justify="right", style="bold")

    hit_delta = f"{(kvguard.cache_hit_rate - baseline.cache_hit_rate) * 100.0:+.1f}%"
    kv_delta = f"{((kvguard.kv_memory_gb - baseline.kv_memory_gb) / baseline.kv_memory_gb) * 100.0:+.1f}%"
    ttft_delta = f"{((kvguard.avg_ttft_ms - baseline.avg_ttft_ms) / baseline.avg_ttft_ms) * 100.0:+.1f}%"
    gpu_delta = f"{((kvguard.gpu_memory_gb - baseline.gpu_memory_gb) / baseline.gpu_memory_gb) * 100.0:+.1f}%"
    cost_delta = f"{((kvguard.estimated_cost_per_hour_usd - baseline.estimated_cost_per_hour_usd) / baseline.estimated_cost_per_hour_usd) * 100.0:+.1f}%"

    table.add_row("Cache Hit Rate", f"{baseline.cache_hit_rate * 100.0:.1f}%", f"{kvguard.cache_hit_rate * 100.0:.1f}%", f"[green]{hit_delta}[/green]")
    table.add_row("KV Memory", f"{baseline.kv_memory_gb:.1f} GB", f"{kvguard.kv_memory_gb:.1f} GB", f"[green]{kv_delta}[/green]")
    table.add_row("TTFT (Time to First Token)", f"{baseline.avg_ttft_ms:.0f} ms", f"{kvguard.avg_ttft_ms:.0f} ms", f"[green]{ttft_delta}[/green]")
    table.add_row("GPU Memory", f"{baseline.gpu_memory_gb:.1f} GB", f"{kvguard.gpu_memory_gb:.1f} GB", f"[green]{gpu_delta}[/green]")
    table.add_row("Estimated Cost", f"${baseline.estimated_cost_per_hour_usd:.2f}/hr", f"${kvguard.estimated_cost_per_hour_usd:.2f}/hr", f"[green]{cost_delta}[/green]")
    table.add_row("Memory Saved", "-", f"{kvguard.memory_saved_gb:.1f} GB", f"[green]+{kvguard.memory_saved_gb:.1f} GB[/green]")

    console.print(table)


if __name__ == "__main__":
    fmt = sys.argv[1] if len(sys.argv) > 1 else "table"
    asyncio.run(run_and_print_report(format_type=fmt))
