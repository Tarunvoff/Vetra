import { fetchRecommendations } from "@/lib/api";
import { RecommendationTable } from "@/components/RecommendationTable";

export const dynamic = "force-dynamic";

export default async function RecommendationsPage() {
  const recs = await fetchRecommendations();

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>Intelligent Recommendations</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.25rem" }}>
          Explainable, rule-based and predictive policies for KV block retention, offloading, and eviction.
        </p>
      </div>

      <RecommendationTable recommendations={recs} />
    </div>
  );
}
