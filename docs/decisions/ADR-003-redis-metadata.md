# ADR-003: Redis as Metadata Repository with In-Memory Fallback

## Status
Accepted

## Context
Metadata operations (tracking block access, hit counts, and tenant assignments) must be ultra-low latency without storing massive GPU KV tensors in Redis.

## Decision
Store lightweight JSON metadata headers and indices in Redis. Actual tensors remain in GPU/Host RAM. Provide an `InMemoryMetadataRepository` fallback for zero-dependency local development and testing.

## Consequences
- Fast sub-millisecond metadata tracking.
- Seamless developer onboarding without requiring a live Redis daemon.
