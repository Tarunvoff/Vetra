"""FastAPI Application Server for the KVGuard Control Plane."""

from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from kvguard.api.dependencies import ServiceContainer, get_container, set_container
from kvguard.api.routes import (
    benchmarks_router,
    cache_router,
    health_router,
    optimization_router,
    policies_router,
    recommendations_router,
    security_router,
    stats_router,
)
from kvguard.config import Settings, load_settings
from kvguard.exceptions import KVGuardError
from kvguard.telemetry.metrics import export_prometheus_metrics
from kvguard.version import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = get_container()
    await container.initialize()
    yield
    await container.shutdown()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Application factory for KVGuard FastAPI control plane."""
    resolved_settings = settings or load_settings()
    container = ServiceContainer(settings=resolved_settings)
    set_container(container)

    app = FastAPI(
        title="KVGuard Control Plane API",
        description="Intelligent Key-Value (KV) Cache Control Plane for LLM Inference Engines",
        version=__version__,
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.api.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler
    @app.exception_handler(KVGuardError)
    async def kvguard_exception_handler(request: Request, exc: KVGuardError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": exc.__class__.__name__, "message": exc.message, "details": exc.details},
        )

    # Prometheus Metrics Endpoint
    @app.get("/metrics", tags=["Observability"])
    async def get_metrics():
        return Response(content=export_prometheus_metrics(), media_type="text/plain")

    # API Version 1 Routes
    api_v1_prefix = "/api/v1"
    app.include_router(health_router, prefix=api_v1_prefix)
    app.include_router(stats_router, prefix=api_v1_prefix)
    app.include_router(recommendations_router, prefix=api_v1_prefix)
    app.include_router(cache_router, prefix=api_v1_prefix)
    app.include_router(policies_router, prefix=api_v1_prefix)
    app.include_router(security_router, prefix=api_v1_prefix)
    app.include_router(optimization_router, prefix=api_v1_prefix)
    app.include_router(benchmarks_router, prefix=api_v1_prefix)

    # Root redirect / status
    @app.get("/", tags=["General"])
    async def root():
        return {
            "name": "KVGuard Control Plane",
            "version": __version__,
            "docs_url": "/docs",
            "health_url": f"{api_v1_prefix}/health",
            "metrics_url": "/metrics",
        }

    return app


app = create_app()
