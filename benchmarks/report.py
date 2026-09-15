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
from benchmarks.runners.vetra import run_vetra_benchmark


def generate_markdown_report(baseline, vetra) -> str:
    hit_delta = f"{(vetra.cache_hit_rate - baseline.cache_hit_rate) * 100.0:+.1f}%"
    kv_delta = f"{((vetra.kv_memory_gb - baseline.kv_memory_gb) / baseline.kv_memory_gb) * 100.0:+.1f}%"
    ttft_delta = f"{((vetra.avg_ttft_ms - baseline.avg_ttft_ms) / baseline.avg_ttft_ms) * 100.0:+.1f}%"
    gpu_delta = f"{((vetra.gpu_memory_gb - baseline.gpu_memory_gb) / baseline.gpu_memory_gb) * 100.0:+.1f}%"
    cost_delta = f"{((vetra.estimated_cost_per_hour_usd - baseline.estimated_cost_per_hour_usd) / baseline.estimated_cost_per_hour_usd) * 100.0:+.1f}%"

    md = f"""# Vetra Benchmark Evaluation Report

**Workload**: `{vetra.workload}` | **Requests**: `{vetra.total_requests}` | **Status**: `{'SIMULATION' if vetra.is_simulation else 'LIVE'}`

| Metric | Baseline | Vetra | Delta |
| :--- | :--- | :--- | :--- |
| **Cache Hit Rate** | {baseline.cache_hit_rate * 100.0:.1f}% | {vetra.cache_hit_rate * 100.0:.1f}% | **{hit_delta}** |
| **KV Memory** | {baseline.kv_memory_gb:.1f} GB | {vetra.kv_memory_gb:.1f} GB | **{kv_delta}** |
| **TTFT** | {baseline.avg_ttft_ms:.0f} ms | {vetra.avg_ttft_ms:.0f} ms | **{ttft_delta}** |
| **GPU Memory** | {baseline.gpu_memory_gb:.1f} GB | {vetra.gpu_memory_gb:.1f} GB | **{gpu_delta}** |
| **Estimated Cost** | ${baseline.estimated_cost_per_hour_usd:.2f}/hr | ${vetra.estimated_cost_per_hour_usd:.2f}/hr | **{cost_delta}** |
| **Memory Saved** | — | {vetra.memory_saved_gb:.1f} GB | **+{vetra.memory_saved_gb:.1f} GB** |
"""
    return md


async def run_and_print_report(format_type: str = "table"):
    console = Console()
    baseline = await run_baseline_benchmark(workload_type="mixed", num_requests=50)
    vetra = await run_vetra_benchmark(workload_type="mixed", num_requests=50)

    if format_type == "json":
        data = {
            "baseline": baseline.model_dump(),
            "vetra": vetra.model_dump(),
        }
        print(json.dumps(data, indent=2))
        return

    if format_type == "markdown":
        print(generate_markdown_report(baseline, vetra))
        return

    # Rich Table output
    table = Table(title="Vetra Benchmark Evaluation: Baseline vs Vetra (SIMULATION)")
    table.add_column("Metric", style="cyan")
    table.add_column("Baseline", justify="right")
    table.add_column("Vetra", justify="right", style="bold green")
    table.add_column("Delta", justify="right", style="bold")

    hit_delta = f"{(vetra.cache_hit_rate - baseline.cache_hit_rate) * 100.0:+.1f}%"
    kv_delta = f"{((vetra.kv_memory_gb - baseline.kv_memory_gb) / baseline.kv_memory_gb) * 100.0:+.1f}%"
    ttft_delta = f"{((vetra.avg_ttft_ms - baseline.avg_ttft_ms) / baseline.avg_ttft_ms) * 100.0:+.1f}%"
    gpu_delta = f"{((vetra.gpu_memory_gb - baseline.gpu_memory_gb) / baseline.gpu_memory_gb) * 100.0:+.1f}%"
    cost_delta = f"{((vetra.estimated_cost_per_hour_usd - baseline.estimated_cost_per_hour_usd) / baseline.estimated_cost_per_hour_usd) * 100.0:+.1f}%"

    table.add_row("Cache Hit Rate", f"{baseline.cache_hit_rate * 100.0:.1f}%", f"{vetra.cache_hit_rate * 100.0:.1f}%", f"[green]{hit_delta}[/green]")
    table.add_row("KV Memory", f"{baseline.kv_memory_gb:.1f} GB", f"{vetra.kv_memory_gb:.1f} GB", f"[green]{kv_delta}[/green]")
    table.add_row("TTFT (Time to First Token)", f"{baseline.avg_ttft_ms:.0f} ms", f"{vetra.avg_ttft_ms:.0f} ms", f"[green]{ttft_delta}[/green]")
    table.add_row("GPU Memory", f"{baseline.gpu_memory_gb:.1f} GB", f"{vetra.gpu_memory_gb:.1f} GB", f"[green]{gpu_delta}[/green]")
    table.add_row("Estimated Cost", f"${baseline.estimated_cost_per_hour_usd:.2f}/hr", f"${vetra.estimated_cost_per_hour_usd:.2f}/hr", f"[green]{cost_delta}[/green]")
    table.add_row("Memory Saved", "-", f"{vetra.memory_saved_gb:.1f} GB", f"[green]+{vetra.memory_saved_gb:.1f} GB[/green]")

    console.print(table)


if __name__ == "__main__":
    fmt = sys.argv[1] if len(sys.argv) > 1 else "table"
    asyncio.run(run_and_print_report(format_type=fmt))
