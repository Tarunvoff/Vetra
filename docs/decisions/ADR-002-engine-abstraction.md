# ADR-002: Inference Engine Adapter Abstraction

## Status
Accepted

## Context
Multiple modern inference runtimes exist with varying capabilities. We need a unified interface that supports capability discovery and fallback handling.

## Decision
Create `IInferenceEngineAdapter` with concrete implementations:
- `VLLMAdapter` (real Prometheus metrics parsing and health checking)
- `SGLangAdapter` (stub)
- `TensorRTLLMAdapter` (stub)
- `SimulatedEngineAdapter` (full offline simulation)

## Consequences
Enables pluggable engine support with zero codebase rewrites when new engines are onboarded.
