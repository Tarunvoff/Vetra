"""Typed exception hierarchy for KVGuard."""


class KVGuardError(Exception):
    """Base exception for all KVGuard errors."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class EngineConnectionError(KVGuardError):
    """Raised when failing to connect to an inference engine backend."""


class EngineMetricsParseError(KVGuardError):
    """Raised when failing to parse telemetry or metrics from the engine."""


class TelemetryError(KVGuardError):
    """Raised during telemetry collection, aggregation, or normalization."""


class UnsupportedCapabilityError(KVGuardError):
    """Raised when an operation is requested that the engine does not support."""


class PolicyError(KVGuardError):
    """Raised during policy evaluation or constraint verification."""


class StorageError(KVGuardError):
    """Raised when metadata persistence or retrieval fails."""


class ConfigurationError(KVGuardError):
    """Raised on invalid or conflicting configuration."""


class SecurityViolationError(KVGuardError):
    """Raised when a tenant isolation or ACL constraint is violated."""


class SimulationError(KVGuardError):
    """Raised during simulated cache environment execution."""
