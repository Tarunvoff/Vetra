# ADR-004: Explainable Rule-Based Policy Engine (Phase 1)

## Status
Accepted

## Context
Operators require full transparency into why blocks are retained, offloaded, or evicted before trusting an automated control plane.

## Decision
Implement a deterministic rule-based policy engine driven by explainable importance scoring:
`importance = w_recency * recency + w_frequency * frequency + w_reuse * reuse`
Every decision provides a human-readable justification string.

## Consequences
- 100% explainable and debuggable recommendations.
- Stable interface allowing drop-in replacement with learned ML models in Phase 3.
