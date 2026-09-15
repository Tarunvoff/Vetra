"""Typed exception hierarchy for Vetra."""


class VetraError(Exception):
    """Base exception for all Vetra errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class EngineConnectionError(VetraError):
    """Raised when failing to connect to an inference engine backend."""


class EngineMetricsParseError(VetraError):
    """Raised when failing to parse telemetry or metrics from the engine."""


class TelemetryError(VetraError):
    """Raised during telemetry collection, aggregation, or normalization."""


class UnsupportedCapabilityError(VetraError):
    """Raised when an operation is requested that the engine does not support."""


class PolicyError(VetraError):
    """Raised during policy evaluation or constraint verification."""


class StorageError(VetraError):
    """Raised when metadata persistence or retrieval fails."""


class ConfigurationError(VetraError):
    """Raised on invalid or conflicting configuration."""


class SecurityViolationError(VetraError):
    """Raised when a tenant isolation or ACL constraint is violated."""


class SimulationError(VetraError):
    """Raised during simulated cache environment execution."""
