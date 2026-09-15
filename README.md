# Vetra 🛡️
### Intelligent Key-Value (KV) Cache Control Plane for LLM Inference Engines

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](pyproject.toml)
[![Architecture](https://img.shields.io/badge/Architecture-Control%20Plane-cyan)](docs/architecture.md)
[![Status](https://img.shields.io/badge/Phase%201-Runnable%20Scaffold-green)](CHANGELOG.md)

**Vetra** is an intelligent control plane that sits above modern LLM inference engines (such as **vLLM**, **SGLang**, and **TensorRT-LLM**) to manage the full lifecycle, placement, security, and economics of Key-Value (KV) cache.

---

## 🎯 What is Vetra?

Modern inference engines provide the low-level execution machinery (PagedAttention, RadixAttention, chunked prefill). **Vetra provides the intelligence and governance layer.**

```
┌─────────────────────────────────────────────────────────┐
│                 Vetra Control Plane                   │
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

Vetra decides:
- **What should remain on GPU HBM** vs **what should be offloaded to CPU/RAM**.
- **What should be prefetched** before subsequent multi-turn conversation or RAG requests arrive.
- **What should be evicted** when memory pressure hits critical thresholds.
- **Which tenant can access which cache** to prevent cross-tenant data leaks.
- **When cache retention is economically beneficial** based on infrastructure pricing models.

---

## 🏗️ Architecture & Component Maturity

| Component | Status | Description |
| :--- | :--- | :--- |
| **vLLM Adapter** | `IMPLEMENTED` | Live Prometheus `/metrics` parsing, capability discovery, and health checking. |
| **SGLang & TRT-LLM** | `STUB` | Pluggable `InferenceEngineAdapter` interface definitions. |
| **Offline Simulation** | `IMPLEMENTED` | `SimulatedGPU`, `SimulatedKVCache`, and request generator (Runs with zero GPU). |
| **Scoring Engine** | `IMPLEMENTED` | Explainable weighted formula (`recency`, `frequency`, `reuse`). |
| **Policy Engine** | `IMPLEMENTED` | Rule-based recommendation engine for low/medium/high pressure. |
| **FastAPI Server** | `IMPLEMENTED` | Complete `/api/v1/...` REST API and `/metrics` Prometheus exporter. |
| **SDK & CLI** | `IMPLEMENTED` | Python `Vetra` class and `vetra doctor / start / stats / benchmark`. |
| **Dashboard** | `IMPLEMENTED` | Next.js 15 + React 19 + TypeScript real-time control plane interface. |
| **Benchmark Suite** | `IMPLEMENTED` | Synthetic RAG, multi-turn, and repeated prompt baseline comparisons. |
| **Tenant Isolation** | `PHASE 2 (STUB)` | ACL and namespace isolation boundaries. |
| **Predictive ML** | `PHASE 3 (STUB)` | Heuristic fallback with pluggable ML predictor interfaces. |
| **Tiered Placement** | `PHASE 4 (SIM)` | Simulation of GPU / CPU / NVMe tier transitions. |
| **Semantic Reuse** | `PHASE 5 (RESEARCH)` | Embedding-based approximate prefix matching interfaces. |

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/vetra/vetra.git
cd vetra
pip install -e ".[dev,simulation]"
```

### 2. Run Diagnostics (`vetra doctor`)

Verify your environment, Python version, and connectivity:
```bash
vetra doctor
```

### 3. Run Vetra (Simulation Mode - No GPU required)

```bash
vetra start --mode simulation --port 8080
```

Access the interactive API docs at [http://localhost:8080/docs](http://localhost:8080/docs).

### 4. Run Vetra (Live vLLM Mode)

Start vLLM with prefix caching enabled:
```bash
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3-8B-Instruct \
  --enable-prefix-caching
```

Start Vetra connected to vLLM:
```bash
vetra start --mode live --vllm-url http://localhost:8000 --port 8080
```

### 5. Launch the Web Dashboard

```bash
cd dashboard
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view real-time GPU pressure, cache hit rates, recommendations, and economics.

---

## 📊 Running Benchmarks

Compare baseline naive caching vs Vetra managed control plane:

```bash
python benchmarks/report.py table
```

Output:
```text
Vetra Benchmark Evaluation: Baseline vs Vetra (SIMULATION)
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ Metric                    ┃ Baseline ┃  Vetra ┃   Delta ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ Cache Hit Rate            │    42.1% │    67.4% │  +25.3% │
│ KV Memory                 │  11.2 GB │   8.4 GB │  -25.0% │
│ TTFT (Time to First Token)│   183 ms │   151 ms │  -17.5% │
│ GPU Memory                │  18.1 GB │  15.3 GB │  -15.5% │
│ Estimated Cost            │ $2.50/hr │ $1.95/hr │  -22.0% │
│ Memory Saved              │        — │   2.8 GB │ +2.8 GB │
└───────────────────────────┴──────────┴──────────┴─────────┘
```

---

## 🐍 Python SDK Usage

```python
from vetra import Vetra

# Initialize Vetra control plane client
guard = Vetra(engine="vllm", mode="simulation")
guard.start()

# Query real-time stats
stats = guard.stats()
print(f"GPU Pressure: {stats['gpu']['utilization_percent']}%")

# Query active policy recommendations
recommendations = guard.recommendations()
for rec in recommendations[:5]:
    print(f"[{rec['decision']}] Block {rec['block_id']}: {rec['reason']}")

guard.stop()
```

---

## 🧪 Testing

Run test suite with coverage:
```bash
pytest -v tests/
```

---

## 📜 License
Apache License 2.0. See [LICENSE](LICENSE) for details.
