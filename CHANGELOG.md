# Changelog

All notable changes to the Vetra project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-16

### Added
- **Core Architecture**: Base models (`KVBlockStats`, `UnifiedDecision`, `Recommendation`, `GPUStats`, `RequestStats`, `EngineCapabilities`).
- **Engine Adapters**: `InferenceEngineAdapter` interface with live `VLLMAdapter` (Prometheus metrics & capability detection) and stubbed `SGLangAdapter` / `TensorRTLLMAdapter`.
- **Telemetry System**: Real-time metric aggregator, normalizer, and Prometheus exporter (`/metrics`).
- **Storage Layer**: `CacheMetadataRepository` with `RedisMetadataRepository` and in-memory fallback.
- **Explainable Scoring Engine**: Weighted recency, frequency, and reuse formula with configurable weights.
- **Policy Engine**: Rule-based recommendation engine for low/medium/high GPU memory pressure.
- **Simulation Mode**: Full offline simulation engine (`SimulatedKVCache`, `SimulatedGPU`, `SimulatedRequest`) for testing without GPU/vLLM.
- **FastAPI Control Plane**: Versioned API (`/api/v1/health`, `/stats`, `/recommendations`, `/policies`, `/security`, `/optimization`, `/benchmarks`).
- **CLI Suite**: `vetra doctor`, `start`, `stats`, `recommendations`, `benchmark`, `config`.
- **Benchmark Suite**: Synthetic workloads (Multi-Turn, RAG, Repeated Prompts) comparing baseline vs Vetra.
- **Web Dashboard**: Next.js + TypeScript dashboard with live/simulation telemetry and before-after comparisons.
- **Architectural Stubs for Phases 2–5**: Tenant isolation, predictive ML scorers, prefetching, adaptive quantization simulation, research modules.
