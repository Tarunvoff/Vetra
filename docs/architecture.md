# KVGuard Architecture Specification

## 1. Problem Statement
Modern Large Language Model (LLM) inference engines (such as vLLM, SGLang, and TensorRT-LLM) manage high token throughput and multi-turn context via PagedAttention and RadixAttention. However, as prompt lengths scale to 128k+ tokens and concurrent multi-tenant workloads surge, KV cache memory quickly exhausts high-bandwidth GPU memory (HBM), causing GPU thrashing, request stalls, and excessive latency.

Existing systems provide the low-level KV cache execution machinery (memory allocators and paging kernels). **KVGuard provides the control plane intelligence and governance layer.**

## 2. KVGuard Core Architecture
KVGuard operates strictly as a policy and governance control plane, decoupled from the underlying inference engines:

```
┌─────────────────────────────────────────────────────────┐
│                 KVGuard Control Plane                   │
│                                                         │
│  [ Observe ] ──> [ Understand ] ──> [ Secure / Decide ]  │
└────────────────────────────┬────────────────────────────┘
                             │
                  Unified Decision Stream
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               Inference Engine Adapters                 │
│         (vLLM / SGLang / TensorRT-LLM / Sim)            │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               Physical Hardware Tiers                   │
│          GPU HBM3  <──>  Host RAM  <──>  NVMe-oF         │
└─────────────────────────────────────────────────────────┘
```

## 3. Comparison: Execution Engines vs Control Plane

| Capability | Underlying Engines (vLLM, SGLang, LMCache) | KVGuard Control Plane |
| :--- | :--- | :--- |
| **Role** | Execution / Data Plane | Intelligence / Policy / Control Plane |
| **KV Tensors** | Directly allocates and mutates in GPU memory | Tracks metadata and access patterns only |
| **Scheduling** | Low-level token forward pass batching | High-level placement, retention & tenant quotas |
| **Security** | Process-level single tenant | Cross-tenant isolation, ACLs, and audit trails |
| **Cost Optimization** | None | Economic cost modeling & ROI trade-offs |

## 4. Architectural Evolution across Product Phases
- **Phase 1 (Foundation - RUNNABLE)**: Real vLLM Prometheus metrics telemetry, explainable rule-based scoring (recency, frequency, reuse), FastAPI control plane, Redis metadata store, offline simulation engine, and benchmarking framework.
- **Phase 2 (Security)**: Tenant namespaces, strict isolation boundaries, ACL rule engine, TTL enforcement, and audit logs.
- **Phase 3 (Intelligence)**: Machine learning predictive reuse models, sequence classifiers, and adaptive workload policies.
- **Phase 4 (Optimization)**: Adaptive quantization simulation (INT8/INT4), hierarchical tiered placement planning (GPU -> CPU -> Remote), and prefetch planners.
- **Phase 5 (Research)**: Semantic approximate prefix reuse, position-independent RoPE realignment, multimodal KV cache, and distributed CXL/RDMA memory pooling.
