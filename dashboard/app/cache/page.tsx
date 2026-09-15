import { fetchStatsOverview } from "@/lib/api";
import { MetricCard } from "@/components/MetricCard";

export const dynamic = "force-dynamic";

export default async function CachePage() {
  const stats = await fetchStatsOverview();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>KV Cache Sizing & Placement</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.25rem" }}>
          Block allocation, prefix tree retention, and physical tier distribution.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1.25rem" }}>
        <MetricCard
          title="GPU Cache Usage"
          value={`${((stats.cache_stats.gpu_cache_usage_factor || 0.85) * 100).toFixed(1)}%`}
          subtitle="Direct High-Bandwidth Memory (HBM)"
          progressPercent={(stats.cache_stats.gpu_cache_usage_factor || 0.85) * 100}
        />
        <MetricCard
          title="CPU Cache Usage"
          value={`${((stats.cache_stats.cpu_cache_usage_factor || 0.22) * 100).toFixed(1)}%`}
          subtitle="Offloaded Host System RAM Tier"
          progressPercent={(stats.cache_stats.cpu_cache_usage_factor || 0.22) * 100}
          progressColor="#4facfe"
        />
        <MetricCard
          title="Total Blocks Tracked"
          value={stats.total_blocks_tracked}
          subtitle="16 tokens / block (128 KB standard)"
        />
      </div>

      <div className="glass-card">
        <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>Cache Hierarchy Tiers</h3>
        <table>
          <thead>
            <tr>
              <th>Tier</th>
              <th>Medium</th>
              <th>Bandwidth</th>
              <th>Status</th>
              <th>Policy Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ fontWeight: 600, color: "#00f2fe" }}>Tier 0</td>
              <td>GPU HBM3</td>
              <td>3.35 TB/s</td>
              <td><span className="badge badge-live">Active</span></td>
              <td>Retain Top 40% High-Importance Blocks</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: "#4facfe" }}>Tier 1</td>
              <td>Host DDR5 RAM</td>
              <td>128 GB/s</td>
              <td><span className="badge badge-live">Active</span></td>
              <td>Proactive PCIe Offload & Async Prefetch</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: "#f59e0b" }}>Tier 2</td>
              <td>Remote NVMe-oF</td>
              <td>12.5 GB/s</td>
              <td><span className="badge badge-sim">Simulated</span></td>
              <td>Session Resurrection Archive</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
