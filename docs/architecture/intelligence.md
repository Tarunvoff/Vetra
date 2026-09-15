# Intelligence & Predictive Policies (Phase 3)

The intelligence layer predicts future cache utilization patterns.

## Components
- **Reuse Predictor**: Heuristic scoring (Phase 1) transitioning to learned ML predictors (Phase 3).
- **Workload Classifier**: Classifies traffic into RAG, Multi-Turn, Repeated Prompts, or General.
- **Adaptive Policy**: Dynamically adjusts eviction and offloading thresholds based on active workload dynamics.
