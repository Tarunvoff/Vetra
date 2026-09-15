"""Hierarchical configuration system using Pydantic Settings and YAML support."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from kvguard.core.enums import EngineType, ExecutionMode


class VLLMConfig(BaseModel):
    """vLLM backend connectivity settings."""

    base_url: str = "http://localhost:8000"
    metrics_path: str = "/metrics"
    health_path: str = "/health"
    timeout_seconds: float = 5.0


class RedisConfig(BaseModel):
    """Redis metadata storage configuration."""

    url: str = "redis://localhost:6379/0"
    key_prefix: str = "kvguard:"
    use_in_memory_fallback: bool = True
    connection_timeout_seconds: float = 2.0


class APIConfig(BaseModel):
    """Control plane REST API server settings."""

    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "INFO"
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])


class TelemetryConfig(BaseModel):
    """Telemetry aggregation parameters."""

    interval_seconds: float = 2.0
    buffer_size: int = 1000
    enable_prometheus_export: bool = True


class ScoringConfig(BaseModel):
    """Explainable importance scoring weights."""

    recency_weight: float = 0.4
    frequency_weight: float = 0.3
    reuse_weight: float = 0.3
    decay_half_life_seconds: float = 300.0


class PolicyConfig(BaseModel):
    """Policy thresholds and decision rules."""

    gpu_memory_threshold: float = 0.85
    gpu_pressure_high: float = 0.90
    gpu_pressure_medium: float = 0.75
    cpu_memory_threshold: float = 0.80
    min_importance_to_keep: float = 0.60
    min_importance_to_offload: float = 0.25


class EconomicsConfig(BaseModel):
    """Infrastructure cost parameters (USD)."""

    gpu_cost_per_hour: float = 2.50
    cpu_cost_per_hour: float = 0.40
    storage_cost_per_gb_month: float = 0.05
    network_cost_per_gb: float = 0.01


class FeaturesConfig(BaseModel):
    """Product phase feature flags."""

    enable_security: bool = False
    enable_intelligence: bool = True
    enable_optimization: bool = False
    enable_research: bool = False


class Settings(BaseSettings):
    """Global configuration settings for KVGuard."""

    model_config = SettingsConfigDict(
        env_prefix="KVGUARD_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    environment: str = "development"
    execution_mode: ExecutionMode = ExecutionMode.SIMULATION
    dry_run: bool = True
    engine: EngineType = EngineType.VLLM

    vllm: VLLMConfig = Field(default_factory=VLLMConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    telemetry: TelemetryConfig = Field(default_factory=TelemetryConfig)
    scoring: ScoringConfig = Field(default_factory=ScoringConfig)
    policy: PolicyConfig = Field(default_factory=PolicyConfig)
    economics: EconomicsConfig = Field(default_factory=EconomicsConfig)
    features: FeaturesConfig = Field(default_factory=FeaturesConfig)

    @classmethod
    def from_yaml(cls, yaml_path: str | Path) -> Settings:
        """Load configuration from a YAML file, overlaid with environment variables."""
        path = Path(yaml_path)
        if not path.exists():
            return cls()

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)


def load_settings(config_path: Optional[str] = None) -> Settings:
    """Load settings from explicit path, env var, or default location."""
    path_to_try = config_path or os.environ.get("KVGUARD_CONFIG_PATH")
    if path_to_try and Path(path_to_try).exists():
        return Settings.from_yaml(path_to_try)

    # Check default configs
    for default_path in ["configs/development.yaml", "configs/production.yaml"]:
        if Path(default_path).exists():
            return Settings.from_yaml(default_path)

    return Settings()
