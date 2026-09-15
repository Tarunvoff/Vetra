"""Workload generator CLI utility."""

import json
import sys
from pathlib import Path

# Ensure repo root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click
from benchmarks.workloads.mixed import generate_mixed_workload
from benchmarks.workloads.multi_turn import generate_multi_turn_workload
from benchmarks.workloads.rag import generate_rag_workload
from benchmarks.workloads.repeated_prompt import generate_repeated_prompt_workload


@click.command()
@click.option("--type", "wtype", default="mixed", type=click.Choice(["mixed", "multi_turn", "rag", "repeated"]))
@click.option("--output", default="benchmark_trace.json", help="Destination JSON file.")
def main(wtype: str, output: str):
    """Generate reproducible benchmark workload traces."""
    if wtype == "multi_turn":
        trace = generate_multi_turn_workload()
    elif wtype == "rag":
        trace = generate_rag_workload()
    elif wtype == "repeated":
        trace = generate_repeated_prompt_workload()
    else:
        trace = generate_mixed_workload()

    with open(output, "w", encoding="utf-8") as f:
        json.dump(trace, f, indent=2)

    click.echo(f"Generated {len(trace)} requests to {output}")


if __name__ == "__main__":
    main()
