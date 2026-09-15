"""GPU instance hourly pricing and computation models."""

DEFAULT_GPU_HOURLY_RATES = {
    "nvidia_h100": 3.85,
    "nvidia_a100_80gb": 2.50,
    "nvidia_l40s": 1.50,
    "nvidia_a10g": 1.00,
    "generic": 2.00,
}


def estimate_gpu_hourly_cost(device_name: str = "generic", default_rate: float = 2.50) -> float:
    """Lookup standard cloud GPU hourly price based on device signature."""
    dev_lower = device_name.lower()
    for key, rate in DEFAULT_GPU_HOURLY_RATES.items():
        if key in dev_lower:
            return rate
    return default_rate
