import { fetchStatsOverview } from "@/lib/api";
import { MetricCard } from "@/components/MetricCard";

export const dynamic = "force-dynamic";

export default async function OptimizationPage() {
  const stats = await fetchStatsOverview();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>Economics & Cost Optimization</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.25rem" }}>
          Infrastructure pricing models, GPU vs CPU tiering economics, and ROI projections.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1.25rem" }}>
        <MetricCard
          title="GPU Hourly Cost"
          value={`$${stats.cost_breakdown.estimated_cost_per_hour.toFixed(2)}`}
          subtitle="NVIDIA H100 GPU Instance"
        />
        <MetricCard
          title="Projected Savings"
          value={`$${stats.cost_breakdown.estimated_savings_per_hour.toFixed(2)}/hr`}
          subtitle="Through proactive offload & reuse"
          change="22.0% Net Savings"
          isPositive={true}
        />
        <MetricCard
          title="Cost / 1M Tokens"
          value={`$${stats.cost_breakdown.estimated_cost_per_1m_tokens.toFixed(3)}`}
          subtitle="Effective inference serving rate"
        />
      </div>

      <div className="glass-card">
        <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>Economic Cost Model Parameters</h3>
        <table>
          <thead>
            <tr>
              <th>Resource Tier</th>
              <th>Unit Cost (USD)</th>
              <th>Pricing Basis</th>
              <th>Optimization Strategy</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ fontWeight: 600, color: "#00f2fe" }}>NVIDIA H100 HBM3</td>
              <td>$2.50 / hour</td>
              <td>Dedicated instance billing</td>
              <td>Maximize KV block density & hit rate</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: "#4facfe" }}>Host DDR5 Memory</td>
              <td>$0.40 / hour</td>
              <td>System RAM allocation</td>
              <td>Low-cost intermediate overflow tier</td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: "#f59e0b" }}>Remote NVMe-oF</td>
              <td>$0.05 / GB-month</td>
              <td>Block storage capacity</td>
              <td>Long-tail session resumption</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
