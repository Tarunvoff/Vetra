"""Command Line Interface (CLI) for KVGuard control plane management."""

from __future__ import annotations

import asyncio
import os
import sys
import click
import httpx
import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from kvguard.config import load_settings
from kvguard.core.enums import ExecutionMode
from kvguard.version import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="kvguard")
def cli():
    """KVGuard: Key-Value Cache Control Plane for LLM Inference Engines."""
    pass


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host address to bind to.")
@click.option("--port", default=8080, type=int, help="Port to listen on.")
@click.option("--mode", default="simulation", type=click.Choice(["live", "simulation"]), help="Execution mode.")
@click.option("--vllm-url", default="http://localhost:8000", help="vLLM base URL.")
def start(host: str, port: int, mode: str, vllm_url: str):
    """Start the KVGuard Control Plane FastAPI daemon."""
    os.environ["KVGUARD_EXECUTION_MODE"] = mode
    os.environ["KVGUARD_VLLM__BASE_URL"] = vllm_url

    console.print(
        Panel.fit(
            f"[bold green]KVGuard Control Plane v{__version__}[/bold green]\n"
            f"[cyan]Mode:[/cyan] {mode.upper()}\n"
            f"[cyan]Engine:[/cyan] vLLM ({vllm_url})\n"
            f"[cyan]API Endpoint:[/cyan] http://{host}:{port}/api/v1\n"
            f"[cyan]Prometheus Metrics:[/cyan] http://{host}:{port}/metrics\n"
            f"[cyan]API Documentation:[/cyan] http://{host}:{port}/docs",
            title="Starting KVGuard Control Plane",
            border_style="green",
        )
    )

    from kvguard.api.server import app
    uvicorn.run(app, host=host, port=port, log_level="info")


@cli.command()
@click.option("--api-url", default="http://localhost:8080/api/v1", help="KVGuard API base URL.")
def doctor(api_url: str):
    """Diagnose environment, connectivity, Python, Redis, and vLLM status."""
    console.print(f"[bold blue]KVGuard Doctor v{__version__}[/bold blue]\n")
    table = Table(title="System & Dependency Health Check")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="bold")
    table.add_column("Details")

    # 1. Python Version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 11):
        table.add_row("Python", "[green]PASS[/green]", f"Python {py_ver} (>=3.11 required)")
    else:
        table.add_row("Python", "[red]FAIL[/red]", f"Python {py_ver} (<3.11 unsupported)")

    # 2. Redis Check
    settings = load_settings()
    try:
        import redis
        r = redis.from_url(settings.redis.url, socket_timeout=1.0)
        r.ping()
        table.add_row("Redis Metadata Store", "[green]PASS[/green]", f"Connected to {settings.redis.url}")
    except Exception as e:
        if settings.redis.use_in_memory_fallback:
            table.add_row("Redis Metadata Store", "[yellow]FALLBACK[/yellow]", f"In-Memory fallback active ({e})")
        else:
            table.add_row("Redis Metadata Store", "[red]FAIL[/red]", f"Unreachable: {e}")

    # 3. vLLM Engine Check
    try:
        resp = httpx.get(f"{settings.vllm.base_url}{settings.vllm.health_path}", timeout=1.0)
        if resp.status_code == 200:
            table.add_row("vLLM Backend", "[green]PASS[/green]", f"Online at {settings.vllm.base_url}")
        else:
            table.add_row("vLLM Backend", "[yellow]DEGRADED[/yellow]", f"HTTP {resp.status_code}")
    except Exception:
        table.add_row("vLLM Backend", "[yellow]SIMULATED[/yellow]", f"Not detected at {settings.vllm.base_url} (Simulation Mode available)")

    # 4. KVGuard API Service
    try:
        resp = httpx.get(f"{api_url}/health", timeout=1.0)
        if resp.status_code == 200:
            table.add_row("KVGuard API", "[green]ONLINE[/green]", f"Responding at {api_url}")
        else:
            table.add_row("KVGuard API", "[yellow]DEGRADED[/yellow]", f"HTTP {resp.status_code}")
    except Exception:
        table.add_row("KVGuard API", "[yellow]OFFLINE[/yellow]", "Start with 'kvguard start'")

    # 5. Dashboard config
    dash_path = os.path.join(os.getcwd(), "dashboard")
    if os.path.exists(dash_path):
        table.add_row("Dashboard Project", "[green]FOUND[/green]", f"{dash_path}")
    else:
        table.add_row("Dashboard Project", "[yellow]MISSING[/yellow]", "Dashboard folder not found in current directory")

    console.print(table)


@cli.command()
@click.option("--api-url", default="http://localhost:8080/api/v1", help="KVGuard API base URL.")
def stats(api_url: str):
    """Display real-time GPU and Cache statistics."""
    try:
        resp = httpx.get(f"{api_url}/stats", timeout=3.0)
        if resp.status_code != 200:
            console.print(f"[red]Error fetching stats: HTTP {resp.status_code}[/red]")
            return
        data = resp.json()
        gpu = data["gpu_stats"]

        table = Table(title="KVGuard Live Telemetry Overview")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold green")

        table.add_row("GPU Device", str(gpu.get("device_name", "N/A")))
        table.add_row("GPU Memory Utilization", f"{gpu.get('utilization_percent', 0.0):.1f}%")
        table.add_row("KV Cache Hit Rate", f"{data.get('cache_hit_rate', 0.0) * 100.0:.1f}%")
        table.add_row("Active Requests", str(data.get("active_requests", 0)))
        table.add_row("Total Blocks Tracked", str(data.get("total_blocks_tracked", 0)))
        table.add_row("Estimated Cost / Hour", f"${data['cost_breakdown']['estimated_cost_per_hour']:.2f}")
        table.add_row("Estimated Savings / Hour", f"${data['cost_breakdown']['estimated_savings_per_hour']:.2f}")

        console.print(table)
    except Exception as e:
        console.print(f"[red]Could not connect to KVGuard API at {api_url}: {e}[/red]")


@cli.command()
@click.option("--api-url", default="http://localhost:8080/api/v1", help="KVGuard API base URL.")
def recommendations(api_url: str):
    """List active KV cache recommendations."""
    try:
        resp = httpx.get(f"{api_url}/recommendations", timeout=3.0)
        if resp.status_code != 200:
            console.print(f"[red]Error: HTTP {resp.status_code}[/red]")
            return

        data = resp.json()
        recs = data.get("recommendations", [])
        table = Table(title=f"KVGuard Active Recommendations (Total: {data.get('total', 0)}, GPU Pressure: {data.get('gpu_pressure', 0.0):.1%})")
        table.add_column("Block ID", style="cyan")
        table.add_column("Decision", style="bold")
        table.add_column("Score", justify="right")
        table.add_column("Reason")

        for r in recs[:15]:
            decision = r["decision"]
            color = "green" if decision == "KEEP" else "yellow" if decision == "OFFLOAD_CPU" else "red"
            table.add_row(
                r["block_id"],
                f"[{color}]{decision}[/{color}]",
                f"{r['score']:.2f}",
                r["reason"],
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Failed to fetch recommendations: {e}[/red]")


@cli.command()
@click.option("--workload", default="mixed", help="Workload type (multi_turn, rag, repeated_prompt, mixed).")
@click.option("--requests", default=50, type=int, help="Number of requests to benchmark.")
def benchmark(workload: str, requests: int):
    """Run baseline vs KVGuard benchmark evaluation."""
    from benchmarks.runners.kvguard import run_kvguard_benchmark
    console.print(f"[bold green]Running KVGuard Benchmark:[/bold green] Workload={workload}, Requests={requests}")
    asyncio.run(run_kvguard_benchmark(workload_type=workload, num_requests=requests))


@cli.command()
def config():
    """Print current effective configuration."""
    settings = load_settings()
    import yaml
    console.print(Panel(yaml.dump(settings.model_dump()), title="KVGuard Effective Configuration", border_style="blue"))


if __name__ == "__main__":
    cli()
