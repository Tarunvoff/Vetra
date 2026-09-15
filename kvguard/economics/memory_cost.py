"""Host system RAM and offload storage cost models."""


def estimate_host_ram_hourly_cost(ram_bytes: int, hourly_rate_per_gb: float = 0.005) -> float:
    """Estimate host RAM cost for offloaded KV cache in USD/hour."""
    ram_gb = ram_bytes / (1024 ** 3)
    return ram_gb * hourly_rate_per_gb
