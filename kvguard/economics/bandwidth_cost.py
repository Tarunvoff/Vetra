"""PCIe / NVLink / Network transfer cost estimation."""


def estimate_transfer_bandwidth_cost(transferred_bytes: int, cost_per_gb: float = 0.01) -> float:
    """Calculate network egress/ingress cost for remote KV cache transfer."""
    gb = transferred_bytes / (1024 ** 3)
    return gb * cost_per_gb
