"""Optional OpenTelemetry distributed tracing integration."""

from typing import Optional

_tracer = None


def get_tracer(service_name: str = "kvguard-control-plane"):
    """Get OpenTelemetry tracer if available, otherwise return no-op mock."""
    global _tracer
    if _tracer is not None:
        return _tracer

    try:
        from opentelemetry import trace
        _tracer = trace.get_tracer(service_name)
    except Exception:
        class NoOpTracer:
            def start_as_current_span(self, name: str, *args, **kwargs):
                from contextlib import nullcontext
                return nullcontext()

        _tracer = NoOpTracer()

    return _tracer
