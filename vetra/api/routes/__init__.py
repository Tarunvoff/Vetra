"""API Route definitions."""

from vetra.api.routes.benchmarks import router as benchmarks_router
from vetra.api.routes.cache import router as cache_router
from vetra.api.routes.health import router as health_router
from vetra.api.routes.optimization import router as optimization_router
from vetra.api.routes.policies import router as policies_router
from vetra.api.routes.recommendations import router as recommendations_router
from vetra.api.routes.security import router as security_router
from vetra.api.routes.stats import router as stats_router

__all__ = [
    "health_router",
    "stats_router",
    "recommendations_router",
    "cache_router",
    "policies_router",
    "security_router",
    "optimization_router",
    "benchmarks_router",
]
