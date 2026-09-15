"""Service Level Objective (SLO) compliance and threshold monitor."""

from kvguard.core.models import PolicyConstraints, RequestStats


class SLOMonitor:
    """Monitors TTFT and latency compliance against configured SLO constraints."""

    @staticmethod
    def check_request_slo(request: RequestStats, constraints: PolicyConstraints) -> bool:
        if constraints.max_ttft_ms is not None and request.ttft_ms is not None:
            if request.ttft_ms > constraints.max_ttft_ms:
                return False
        return True
