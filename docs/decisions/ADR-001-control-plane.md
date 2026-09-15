# ADR-001: Separation of Control Plane from Inference Data Plane

## Status
Accepted

## Context
Inference engines (vLLM, SGLang, TensorRT-LLM) evolve rapidly. Directly forking or embedding custom cache allocators inside engine engines creates high maintenance burden and fragile coupling.

## Decision
Vetra operates strictly as an out-of-process control plane. The inference engine handles raw forward passes and memory allocation; Vetra monitors telemetry, scores block utility, and issues placement recommendations.

## Consequences
- **Positive**: Engine agnostic; no monkey-patching of engine internals.
- **Negative**: Phase 1 is recommendation-only until engines expose mutation control endpoints.
