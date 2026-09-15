/**
 * KVGuard Control Plane API Client with Simulation Fallback
 */

export interface GPUStats {
  total_memory_bytes: number;
  used_memory_bytes: number;
  free_memory_bytes: number;
  utilization_percent: number;
  kv_memory_bytes: number;
  kv_utilization_percent: number;
  device_name: string;
}

export interface Recommendation {
  block_id: string;
  tenant_id: string;
  decision: "KEEP" | "OFFLOAD_CPU" | "PREFETCH" | "EVICT" | "NO_OP";
  score: number;
  reason: string;
  expected_memory_saving_bytes: number;
  expected_latency_delta_ms: number;
  confidence: number;
}

export interface StatsOverview {
  gpu_stats: GPUStats;
  cache_stats: {
    gpu_cache_usage_factor?: number;
    cpu_cache_usage_factor?: number;
    cache_hit_rate?: number;
    num_requests_running?: number;
    num_requests_waiting?: number;
    is_simulation?: boolean;
  };
  active_requests: number;
  total_blocks_tracked: number;
  cache_hit_rate: number;
  cost_breakdown: {
    estimated_cost_per_hour: number;
    estimated_cost_per_1m_tokens: number;
    estimated_savings_per_hour: number;
    is_simulated: boolean;
  };
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080/api/v1";

export async function fetchStatsOverview(): Promise<StatsOverview> {
  try {
    const res = await fetch(`${API_BASE}/stats`, { cache: "no-store" });
    if (res.ok) {
      return await res.json();
    }
  } catch {
    // Return simulated state when API server is offline
  }

  return {
    gpu_stats: {
      total_memory_bytes: 80 * 1024 * 1024 * 1024,
      used_memory_bytes: 68 * 1024 * 1024 * 1024,
      free_memory_bytes: 12 * 1024 * 1024 * 1024,
      utilization_percent: 85.0,
      kv_memory_bytes: 42 * 1024 * 1024 * 1024,
      kv_utilization_percent: 72.5,
      device_name: "Simulated NVIDIA H100 80GB (Offline Demo)",
    },
    cache_stats: {
      gpu_cache_usage_factor: 0.85,
      cpu_cache_usage_factor: 0.22,
      cache_hit_rate: 0.674,
      num_requests_running: 12,
      num_requests_waiting: 1,
      is_simulation: true,
    },
    active_requests: 12,
    total_blocks_tracked: 128,
    cache_hit_rate: 0.674,
    cost_breakdown: {
      estimated_cost_per_hour: 2.5,
      estimated_cost_per_1m_tokens: 0.18,
      estimated_savings_per_hour: 0.55,
      is_simulated: true,
    },
  };
}

export async function fetchRecommendations(): Promise<Recommendation[]> {
  try {
    const res = await fetch(`${API_BASE}/recommendations`, { cache: "no-store" });
    if (res.ok) {
      const data = await res.json();
      return data.recommendations || [];
    }
  } catch {
    // fallback
  }

  return [
    {
      block_id: "sim_blk_001",
      tenant_id: "tenant_alpha",
      decision: "KEEP",
      score: 0.88,
      reason: "High frequency access in active multi-turn session.",
      expected_memory_saving_bytes: 0,
      expected_latency_delta_ms: 0,
      confidence: 0.95,
    },
    {
      block_id: "sim_blk_002",
      tenant_id: "tenant_beta",
      decision: "OFFLOAD_CPU",
      score: 0.42,
      reason: "Moderate importance under 85% GPU memory pressure; tiering to host RAM.",
      expected_memory_saving_bytes: 131072,
      expected_latency_delta_ms: 12.5,
      confidence: 0.9,
    },
    {
      block_id: "sim_blk_003",
      tenant_id: "tenant_alpha",
      decision: "PREFETCH",
      score: 0.79,
      reason: "Subsequent RAG turn predicted; prefetching CPU block to GPU.",
      expected_memory_saving_bytes: 0,
      expected_latency_delta_ms: -18.0,
      confidence: 0.85,
    },
    {
      block_id: "sim_blk_004",
      tenant_id: "tenant_gamma",
      decision: "EVICT",
      score: 0.14,
      reason: "Idle TTL threshold elapsed and low reuse score (< 0.20).",
      expected_memory_saving_bytes: 131072,
      expected_latency_delta_ms: 60.0,
      confidence: 0.98,
    },
  ];
}
