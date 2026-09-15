import { ComparisonTable } from "@/components/ComparisonTable";
import { MetricCard } from "@/components/MetricCard";

export const dynamic = "force-dynamic";

export default function BenchmarksPage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>Inference Benchmark Evaluation</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.25rem" }}>
          Reproducible comparisons of baseline vs KVGuard policy engine on multi-turn and RAG workloads.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1.25rem" }}>
        <MetricCard
          title="Hit Rate Gain"
          value="+25.3%"
          subtitle="Baseline 42.1% -> KVGuard 67.4%"
          isPositive={true}
        />
        <MetricCard
          title="TTFT Reduction"
          value="-17.5%"
          subtitle="Baseline 183ms -> KVGuard 151ms"
          isPositive={true}
        />
        <MetricCard
          title="Memory Saved"
          value="2.8 GB"
          subtitle="Baseline 11.2GB -> KVGuard 8.4GB"
          isPositive={true}
        />
      </div>

      <ComparisonTable />
    </div>
  );
}
