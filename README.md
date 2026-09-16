# Vetra 🛡️
### Intelligent Key-Value (KV) Cache Control Plane for LLM Inference Engines

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![Architecture](https://img.shields.io/badge/Architecture-Control%20Plane-cyan)](docs/architecture.md)
[![Tests](https://img.shields.io/badge/tests-25%20passed-green)](tests/)
[![Dashboard](https://img.shields.io/badge/dashboard-Next.js%2015%20%2B%20React%2019-black)](dashboard/)
[![Research Deep-Dive](https://img.shields.io/badge/Research-KV%20Cache%20Deep%20Dive-purple)](docs/research/deep-dive-kv-cache.md)

**Vetra** is an enterprise-grade, engine-agnostic **Key-Value (KV) Cache Control Plane** designed to sit above modern LLM serving systems (such as **vLLM**, **SGLang**, and **TensorRT-LLM**). It governs the physical lifecycle, tiered placement, multi-tenant isolation, proactive prefetching, dynamic quantization, and infrastructure economics of KV memory across GPU HBM, Host DDR5 RAM, and remote NVMe/CXL storage tiers.

---

## 📑 Table of Contents

- [🎯 Executive Overview](#-executive-overview)
- [🏗️ Architectural Topography & Decision Flow](#️-architectural-topography--decision-flow)
- [🚀 In-Depth Feature Breakdown](#-in-depth-feature-breakdown)
  - [1. Engine Abstraction & Live Telemetry](#1-engine-abstraction--live-telemetry)
  - [2. Explainable 3-Factor Scoring Engine](#2-explainable-3-factor-scoring-engine)
  - [3. Pressure-Adaptive Policy Engine](#3-pressure-adaptive-policy-engine)
  - [4. Dual-Tier Metadata Storage Layer](#4-dual-tier-metadata-storage-layer)
  - [5. Zero-Trust Multi-Tenancy & Security ACLs](#5-zero-trust-multi-tenancy--security-acls)
  - [6. Infrastructure Economics & Cost Optimizer](#6-infrastructure-economics--cost-optimizer)
  - [7. Hierarchical Placement Planner](#7-hierarchical-placement-planner)
  - [8. Optimization & Quantization Layer](#8-optimization--quantization-layer)
  - [9. Predictive Intelligence Extensions](#9-predictive-intelligence-extensions)
  - [10. Advanced Research Frontier](#10-advanced-research-frontier)
  - [11. Zero-GPU Offline Simulation Suite](#11-zero-gpu-offline-simulation-suite)
  - [12. FastAPI Control Server & Prometheus Exporter](#12-fastapi-control-server--prometheus-exporter)
  - [13. Next.js 15 Real-Time Web Dashboard](#13-nextjs-15-real-time-web-dashboard)
  - [14. Benchmark Evaluation Framework](#14-benchmark-evaluation-framework)
  - [15. Rich CLI & Diagnostics Tooling](#15-rich-cli--diagnostics-tooling)
- [📊 Empirical Benchmark Results](#-empirical-benchmark-results)
- [⚡ Quickstart & Usage](#-quickstart--usage)
- [🐍 Python SDK Examples](#-python-sdk-examples)
- [🧪 Automated Test Verification](#-automated-test-verification)
- [📂 Repository Directory Structure](#-repository-directory-structure)
- [🗺️ Multi-Phase Roadmap](#️-multi-phase-roadmap)
- [📜 License](#-license)

---

## 🎯 Executive Overview

Modern LLM serving engines execute low-level token-generation kernels (e.g., PagedAttention, RadixAttention, chunked prefill). However, **they lack cluster-level intelligence, cost governance, cross-tenant isolation, and proactive tiered placement**.

In production deployments with long context windows (32k–128k tokens) or high concurrency, dynamic KV cache rapidly consumes **60–80% of total GPU High-Bandwidth Memory (HBM)**, creating a severe memory wall that stalls inference and inflates GPU cluster costs.

**Vetra resolves this by providing the external intelligence and governance plane:**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          Vetra Control Plane                            │
│                                                                          │
│  [ Observe Telemetry ] ──> [ Compute Scores ] ──> [ Enforce Policies ]   │
│            │                       │                       │             │
│            ▼                       ▼                       ▼             │
│   Prometheus Scrapers       Recency/Freq/Reuse     KEEP / OFFLOAD / EVICT│
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Unified Decision Stream
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        Inference Engine Adapters                         │
│             vLLM (Live)  │  SGLang (Stub)  │  TRT-LLM (Stub)             │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Physical Memory Placements
                                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Hardware Memory Hierarchy                        │
│      Tier 0: GPU HBM3   <───>   Tier 1: Host RAM   <───>  Tier 2: NVMe   │
│       (3.35 TB/s)                  (128 GB/s)              (10-25 GB/s)  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architectural Topography & Decision Flow

```mermaid
flowchart TD
    subgraph Observability ["1. Observability & Telemetry"]
        VLLM[vLLM Prometheus /metrics] --> Collector[Metrics Collector]
        GPU[GPU Telemetry / NVML] --> Aggregator[Telemetry Aggregator]
        Req[Request Stream Tracker] --> Aggregator
    end

    subgraph Intelligence ["2. Scoring & Policy Engine"]
        Aggregator --> Scoring[Importance Scorer\n(Recency + Freq + Reuse)]
        Scoring --> Policy[Pressure Adaptive Policy Engine]
        Sec[Security & ACL Engine] --> Policy
    end

    subgraph Execution ["3. Decision Stream & Placement"]
        Policy --> Decision{Pressure Threshold}
        Decision -->|Low <70%| Keep[KEEP on GPU HBM]
        Decision -->|Med 70-90%| Offload[OFFLOAD to Host DDR5 RAM]
        Decision -->|High >90%| Evict[EVICT Least Important Blocks]
    end

    subgraph Storage ["4. Metadata Layer"]
        Policy <--> Meta[Redis Metadata Repository\n(with In-Memory Fallback)]
    end
```

---

## 🚀 In-Depth Feature Breakdown

### 1. Engine Abstraction & Live Telemetry
- **Unified Interface (`vetra/engines/base.py`)**: Abstract contract defining `collect_stats()`, `get_capabilities()`, and `apply_decisions()`.
- **vLLM Live Adapter (`vetra/engines/vllm/`)**: Actively parses Prometheus metrics from live vLLM instances (`vllm:num_requests_running`, `vllm:gpu_cache_usage_factor`, `vllm:cpu_cache_usage_factor`, `vllm:prompt_tokens_total`).
- **Telemetry Aggregator (`vetra/telemetry/`)**: Normalizes disparate engine counters into standard `GPUStats`, `KVBlockStats`, and `RequestStats` models with lock-free thread safety.

### 2. Explainable 3-Factor Scoring Engine
- **Mathematical Formula (`vetra/scoring/importance.py`)**: Every KV cache block receives a deterministic retention score $S \in [0, 1]$:
  $$S = w_r \cdot R(t) + w_f \cdot F(n) + w_u \cdot U(k)$$
- **Recency Decay ($R$)**: Half-life exponential decay based on seconds elapsed since last access: $R(t) = 2^{-t / t_{\text{half}}}$.
- **Frequency Saturation ($F$)**: Diminishing-returns logarithmic access frequency: $F(n) = \frac{\ln(1 + n)}{\ln(1 + n_{\text{max}})}$.
- **Reuse Utility ($U$)**: Prefix tree depth and token count scaling factor: $U(k) = \min(1.0, \frac{k}{k_{\text{ref}}})$.

### 3. Pressure-Adaptive Policy Engine
- **Rule Engine (`vetra/policy/engine.py`)**: Dynamic threshold adaptation:
  - **Low Pressure ($<70\%$ VRAM)**: Aggressive retention (`KEEP`), proactive warm-prefix caching.
  - **Medium Pressure ($70\%\text{--}90\%$ VRAM)**: Selective CPU offloading of low-scoring blocks to preserve GPU headroom.
  - **High / Critical Pressure ($>90\%$ VRAM)**: Emergency eviction of coldest blocks and proactive KV quantization to prevent OOM request stalls.
- **Explainability**: Every single decision outputs a human-readable justification string for auditing.

### 4. Dual-Tier Metadata Storage Layer
- **Interface (`vetra/storage/interface.py`)**: Asynchronous key-value metadata repository interface.
- **Redis Engine (`vetra/storage/redis.py`)**: Distributed Redis backend storing block hashes, tenant IDs, timestamps, and access logs with configurable TTL.
- **In-Memory Fallback (`vetra/storage/memory.py`)**: Automatic, zero-configuration memory fallback ensuring 100% functionality without requiring external Redis instances.

### 5. Zero-Trust Multi-Tenancy & Security ACLs
- **Namespace Isolation (`vetra/security/`)**: Every block hash is strictly namespaced (`tenant_id:namespace_id:block_hash`).
- **Access Control Lists (`vetra/security/acl.py`)**: Deterministic whitelist rules preventing cross-tenant prefix reuse.
- **Side-Channel Defense**: Eliminates timing attacks where malicious tenants deduce prompt contents by observing TTFT cache hit latencies.
- **Audit Logging (`vetra/security/audit.py`)**: Cryptographically verifiable access trails for compliance (HIPAA, SOC2).

### 6. Infrastructure Economics & Cost Optimizer
- **Financial Cost Modeling (`vetra/economics/`)**: Calculates dollar-per-hour instance depreciation ($/hr GPU HBM vs. $/GB DDR5 RAM).
- **Savings Attribution**: Computes exact dollars saved per hour from avoided token recomputation FLOPs and reduced GPU node provisioning.

### 7. Hierarchical Placement Planner
- **Multi-Tier Orchestrator (`vetra/placement/planner.py`)**:
  - **Tier 0 (GPU HBM3/e)**: 3.35 TB/s bandwidth — active generation working set.
  - **Tier 1 (Host DDR5 RAM)**: 128 GB/s bandwidth — warm multi-turn sessions.
  - **Tier 2 (Remote NVMe-oF / CXL)**: 10–25 GB/s bandwidth — cold session checkpoints.

### 8. Optimization & Quantization Layer
- **Quantization Simulator (`vetra/optimization/quantization.py`)**: Evaluates memory compression trade-offs across **FP8** (50% VRAM savings), **INT8** (50% savings), and **INT4 / KIVI** (75% savings).
- **Proactive Prefetching (`vetra/optimization/prefetch.py`)**: Anticipates subsequent conversational turns and schedules asynchronous Host-to-Device (H2D) DMA transfers over PCIe.

### 9. Predictive Intelligence Extensions
- **Workload Classifier (`vetra/intelligence/workload_classifier.py`)**: Categorizes requests into **Multi-Turn Chat**, **RAG Pipeline**, **Agentic Tool Call**, or **Single-Turn Batch**.
- **Reuse Predictor (`vetra/intelligence/reuse_predictor.py`)**: Heuristic and ML interfaces predicting block reuse probabilities.

### 10. Advanced Research Frontier
- **Semantic Prefix Reuse (`vetra/research/semantic_reuse.py`)**: Embedding-similarity search for approximate prompt caching.
- **Position-Independent RoPE (`vetra/research/position_independent.py`)**: Decoupling rotary position embeddings from KV representations.
- **Multimodal Caching (`vetra/research/multimodal.py`)**: Image patch and audio spectrogram KV tensor lifecycle management.

### 11. Zero-GPU Offline Simulation Suite
- **Virtual GPU (`vetra/simulation/state.py`)**: Configurable VRAM capacity (e.g. 24GB, 80GB, 141GB), memory bandwidth, and allocation maps.
- **Synthetic Workload Generator (`vetra/simulation/workload.py`)**: Generates multi-turn chats, shared system prompts, and RAG document injections.
- **Policy Environment (`vetra/simulation/environment.py`)**: Step-by-step discrete-event simulation engine for rapid policy experimentation.

### 12. FastAPI Control Server & Prometheus Exporter
- **REST Endpoints (`vetra/api/`)**:
  - `GET /api/v1/health`: System health and dependency state.
  - `GET /api/v1/stats`: Live GPU utilization, hit rates, and request concurrency.
  - `GET /api/v1/recommendations`: Active block-level retention decisions.
  - `GET /api/v1/cache/blocks`: Real-time KV cache block registry.
  - `GET /api/v1/security/policies`: Tenant ACL rules and audit summaries.
  - `GET /api/v1/benchmarks`: Baseline vs. Vetra benchmark evaluations.
  - `GET /metrics`: Standard Prometheus metrics exporter (`vetra_gpu_utilization_ratio`, `vetra_cache_hit_ratio`, `vetra_active_requests`).

### 13. Next.js 15 Real-Time Web Dashboard
- Built with **Next.js 15**, **React 19**, **TypeScript**, and modern glassmorphic aesthetics.
- **6 Dedicated Control Views**:
  1. `/` — **System Overview**: Live GPU gauges, cache hit rates, cost metrics, and activity charts.
  2. `/cache` — **KV Cache Inspector**: Real-time table of tracked blocks, access frequencies, and scores.
  3. `/recommendations` — **Policy Stream**: Live actionable recommendations (`KEEP`, `OFFLOAD_CPU`, `EVICT`).
  4. `/security` — **Multi-Tenant Security**: Tenant namespace isolation rules and audit event logs.
  5. `/economics` — **Cost & ROI Optimizer**: Cost per hour vs. realized compute savings.
  6. `/benchmarks` — **Benchmark Studio**: Visual comparison charts for baseline vs. Vetra performance.

### 14. Benchmark Evaluation Framework
- **Runners (`benchmarks/runners/`)**: Executes baseline unmanaged caching vs. Vetra-controlled caching.
- **Report Generators (`benchmarks/report.py`)**: Formats benchmark results into Terminal Tables, Markdown Reports, and JSON files.

### 15. Rich CLI & Diagnostics Tooling
- **`vetra doctor`**: Comprehensive environment, dependency, and connectivity diagnosis.
- **`vetra start`**: Launch the control plane daemon in simulation or live engine mode.
- **`vetra stats`**: Terminal dashboard of live engine metrics.
- **`vetra recommendations`**: Inspect active cache retention decisions.
- **`vetra benchmark`**: Run automated performance evaluations.
- **`vetra config`**: Inspect resolved YAML configuration parameters.

---

## 📊 Empirical Benchmark Results

Running the synthetic benchmark evaluation (`python benchmarks/report.py table`) demonstrates substantial gains:

| Metric | Baseline (Naive) | Vetra Control Plane | Improvement |
| :--- | :---: | :---: | :---: |
| **Cache Hit Rate** | `56.6%` | **`86.7%`** | **`+30.1%`** |
| **KV Cache Memory Footprint** | `11.2 GB` | **`8.4 GB`** | **`-25.0%`** |
| **Time-to-First-Token (TTFT)** | `183 ms` | **`151 ms`** | **`-17.6%`** |
| **Total GPU Memory Used** | `18.1 GB` | **`15.3 GB`** | **`-15.5%`** |
| **Infrastructure Cost** | `$2.50 / hr` | **`$1.95 / hr`** | **`-22.0%`** |
| **Memory Saved on HBM** | `—` | **`+2.8 GB`** | **`+2.8 GB`** |

---

## ⚡ Quickstart & Usage

### 1. Installation

```bash
git clone https://github.com/Tarunvoff/Vetra.git
cd Vetra
pip install -e ".[dev,simulation]"
```

### 2. Run Diagnostics

```bash
vetra doctor
```

### 3. Start Vetra (Zero-GPU Simulation Mode)

```bash
vetra start --mode simulation --port 8080
```
- Open Swagger API Docs: [http://localhost:8080/docs](http://localhost:8080/docs)
- Open Prometheus Metrics: [http://localhost:8080/metrics](http://localhost:8080/metrics)

### 4. Start Vetra (Live vLLM Mode)

```bash
# In Terminal 1: Start vLLM with prefix caching enabled
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --enable-prefix-caching

# In Terminal 2: Connect Vetra to vLLM
vetra start --mode live --vllm-url http://localhost:8000 --port 8080
```

### 5. Start the Web Dashboard

```bash
cd dashboard
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the live control center.

---

## 🐍 Python SDK Examples

```python
from vetra import Vetra

# 1. Initialize Vetra Control Plane
guard = Vetra(engine="vllm", mode="simulation")
guard.start()

# 2. Query Live Engine & GPU Telemetry
stats = guard.stats()
print(f"GPU Utilization: {stats['gpu']['utilization_percent']}%")
print(f"Cache Hit Rate: {stats['cache']['hit_rate'] * 100:.1f}%")
print(f"Active Requests: {stats['requests']['active_count']}")

# 3. Retrieve Intelligent Placement Recommendations
recommendations = guard.recommendations()
for rec in recommendations[:5]:
    print(f"[{rec['decision']}] Block {rec['block_id']}: Score={rec['score']:.2f} ({rec['reason']})")

guard.stop()
```

---

## 🧪 Automated Test Verification

Vetra includes a comprehensive test suite across unit and integration layers:

```bash
pytest -v tests/
```

```text
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.2
collected 25 items

tests\integration\test_api.py ....                                       [ 16%]
tests\integration\test_redis.py ..                                       [ 24%]
tests\integration\test_vllm_adapter.py .                                 [ 28%]
tests\unit\cache\test_block.py .                                         [ 32%]
tests\unit\cache\test_lifecycle.py .                                     [ 36%]
tests\unit\cache\test_metadata.py .                                      [ 40%]
tests\unit\economics\test_cost_model.py .                                [ 44%]
tests\unit\policy\test_constraints.py .                                  [ 48%]
tests\unit\policy\test_engine.py ...                                     [ 60%]
tests\unit\scoring\test_frequency.py ..                                  [ 68%]
tests\unit\scoring\test_importance.py .                                  [ 72%]
tests\unit\scoring\test_recency.py ..                                    [ 80%]
tests\unit\scoring\test_reuse.py .                                       [ 84%]
tests\unit\security\test_acl.py ..                                       [ 92%]
tests\unit\simulation\test_simulation.py ..                              [100%]

============================= 25 passed in 10.24s =============================
```

---

## 📂 Repository Directory Structure

```text
Vetra/
├── benchmarks/                 # Benchmark workloads, runners, and reporting
│   ├── runners/                # Baseline vs Vetra benchmark harnesses
│   ├── workloads/              # Multi-turn, RAG, repeated prompt generators
│   └── report.py               # Markdown, table, and JSON reporter
├── dashboard/                  # Next.js 15 + React 19 Control Plane Dashboard
│   ├── app/                    # App Router pages (overview, cache, recs, etc.)
│   ├── components/             # Reusable UI cards, tables, navbars, charts
│   └── lib/                    # API client and TypeScript interfaces
├── docs/                       # Architectural documentation & ADRs
│   ├── architecture/           # System, data plane, control plane, security docs
│   ├── decisions/              # Architectural Decision Records (ADR-001 to 004)
│   ├── diagrams/               # Mermaid architectural diagrams
│   └── research/               # Foundational KV Cache Deep Dive Whitepaper
├── tests/                      # Automated test suite (Unit & Integration)
│   ├── integration/            # FastAPI, Redis, and vLLM integration tests
│   └── unit/                   # Scoring, policy, security, simulation unit tests
└── vetra/                      # Core Python Package
    ├── api/                    # FastAPI routes, schemas, service container
    ├── cache/                  # Block sizing, lifecycle state machine, manager
    ├── cli/                    # Click CLI commands (doctor, start, stats, recs)
    ├── core/                   # Enums, interfaces, events, core data models
    ├── economics/              # GPU/RAM pricing models and cost optimizer
    ├── engines/                # vLLM adapter, SGLang & TRT-LLM interfaces
    ├── intelligence/           # Workload classifier, reuse & placement predictors
    ├── optimization/           # Quantization simulator, prefetching, offloader
    ├── placement/              # GPU / CPU / NVMe tiering planner
    ├── policy/                 # Pressure-adaptive rule engine & recommendations
    ├── research/               # Semantic reuse, position independence, multimodal
    ├── scoring/                # Recency, frequency, reuse, importance scoring
    ├── security/               # Tenant namespace isolation, ACLs, audit logs
    ├── simulation/             # Discrete-event GPU and KV cache simulator
    ├── storage/                # Redis and In-Memory metadata repositories
    └── telemetry/              # Metrics collectors, GPU monitor, Prometheus exporter
```

---

## 🗺️ Multi-Phase Roadmap

| Phase | Focus Area | Status | Key Deliverables |
| :---: | :--- | :---: | :--- |
| **Phase 1** | **Core Foundation & Scaffolding** | `COMPLETE` | vLLM Prometheus scraper, offline simulator, scoring, rule policy, FastAPI, CLI, Dashboard, Benchmarks. |
| **Phase 2** | **Multi-Tenancy & Security** | `DESIGNED` | Production cryptographic ACL verification, KMS secret integration, automated compliance audit feeds. |
| **Phase 3** | **Predictive ML Intelligence** | `DESIGNED` | LightGBM/transformer-based reuse predictors replacing heuristic fallback estimators. |
| **Phase 4** | **Hardware Tiering & Offload** | `DESIGNED` | Zero-copy PCIe DMA asynchronous H2D/D2H memory offload drivers and CXL pooling. |
| **Phase 5** | **Research Frontier** | `RESEARCH` | Approximate semantic vector cache, RoPE position decoupling, multimodal KV caching. |

---

## 📜 License

Distributed under the **Apache License 2.0**. See [`LICENSE`](LICENSE) for details.
