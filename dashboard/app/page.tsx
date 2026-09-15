import { fetchRecommendations, fetchStatsOverview } from "@/lib/api";
import { MetricCard } from "@/components/MetricCard";
import { RecommendationTable } from "@/components/RecommendationTable";
import { ComparisonTable } from "@/components/ComparisonTable";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const stats = await fetchStatsOverview();
  const recs = await fetchRecommendations();

  const gpuUtil = stats.gpu_stats.utilization_percent;
  const kvMemGb = (stats.gpu_stats.kv_memory_bytes / (1024 ** 3)).toFixed(1);
  const totalGpuGb = (stats.gpu_stats.total_memory_bytes / (1024 ** 3)).toFixed(0);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800, letterSpacing: "-0.025em" }}>
          Inference Control Plane Overview
        </h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.25rem" }}>
          Real-time telemetry, memory pressure management, and explainable caching policies.
        </p>
      </div>

      {/* Top Metrics Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1.25rem" }}>
        <MetricCard
          title="GPU Memory Pressure"
          value={`${gpuUtil.toFixed(1)}%`}
          subtitle={`${kvMemGb} GB KV / ${totalGpuGb} GB Total`}
          progressPercent={gpuUtil}
          progressColor={gpuUtil > 85 ? "#ef4444" : gpuUtil > 70 ? "#f59e0b" : "#10b981"}
        />

        <MetricCard
          title="KV Cache Hit Rate"
          value={`${(stats.cache_hit_rate * 100).toFixed(1)}%`}
          subtitle="Target: > 60.0%"
          change="+25.3% vs Naive"
          isPositive={true}
          progressPercent={stats.cache_hit_rate * 100}
          progressColor="#00f2fe"
        />

        <MetricCard
          title="Active Requests"
          value={stats.active_requests}
          subtitle={`Tracking ${stats.total_blocks_tracked} cache blocks`}
        />

        <MetricCard
          title="Est. Savings / Hour"
          value={`$${stats.cost_breakdown.estimated_savings_per_hour.toFixed(2)}`}
          subtitle={`Instance: $${stats.cost_breakdown.estimated_cost_per_hour.toFixed(2)}/hr`}
          change="22% cost reduction"
          isPositive={true}
        />
      </div>

      {/* Benchmark Comparison Table */}
      <ComparisonTable />

      {/* Active Recommendations Table */}
      <RecommendationTable recommendations={recs} />
    </div>
  );
}
