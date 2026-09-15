"""Structured JSON logging for traceable policy decisions and audit events."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include custom extra fields if provided
        if hasattr(record, "structured_data"):
            log_obj.update(record.structured_data)

        return json.dumps(log_obj)


def setup_logging(level: str = "INFO", json_output: bool = True) -> None:
    """Configure root logger with structured JSON formatting."""
    root = logging.getLogger("vetra")
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    if json_output:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
    root.addHandler(handler)


def log_decision_event(
    logger: logging.Logger,
    block_id: str,
    decision: str,
    importance: float,
    gpu_pressure: float,
    reason: str,
) -> None:
    """Convenience helper for structured policy decision logging."""
    extra = {
        "structured_data": {
            "event": "policy_decision",
            "block_id": block_id,
            "decision": decision,
            "importance": round(importance, 3),
            "gpu_pressure": round(gpu_pressure, 3),
            "reason": reason,
        }
    }
    logger.info(f"Policy decision for {block_id}: {decision}", extra=extra)
