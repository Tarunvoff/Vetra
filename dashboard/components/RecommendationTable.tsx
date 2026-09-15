import React from "react";
import { Recommendation } from "@/lib/api";

export function RecommendationTable({ recommendations }: { recommendations: Recommendation[] }) {
  const getBadgeClass = (decision: string) => {
    switch (decision) {
      case "KEEP":
        return "badge badge-keep";
      case "OFFLOAD_CPU":
        return "badge badge-offload";
      case "PREFETCH":
        return "badge badge-prefetch";
      case "EVICT":
        return "badge badge-evict";
      default:
        return "badge";
    }
  };

  return (
    <div className="glass-card" style={{ overflowX: "auto" }}>
      <div style={{ marginBottom: "1rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h3 style={{ fontSize: "1.1rem", fontWeight: 700 }}>Active Policy Decisions & Recommendations</h3>
        <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Total: {recommendations.length}</span>
      </div>

      <table>
        <thead>
          <tr>
            <th>Block ID</th>
            <th>Tenant</th>
            <th>Decision</th>
            <th>Score</th>
            <th>Est. Memory</th>
            <th>Reasoning</th>
          </tr>
        </thead>
        <tbody>
          {recommendations.map((rec) => (
            <tr key={rec.block_id}>
              <td style={{ fontFamily: "monospace", fontSize: "0.85rem", color: "#00f2fe" }}>
                {rec.block_id}
              </td>
              <td style={{ fontSize: "0.85rem" }}>{rec.tenant_id}</td>
              <td>
                <span className={getBadgeClass(rec.decision)}>{rec.decision}</span>
              </td>
              <td style={{ fontWeight: 600 }}>{rec.score.toFixed(2)}</td>
              <td style={{ fontSize: "0.85rem", color: rec.expected_memory_saving_bytes > 0 ? "#10b981" : "inherit" }}>
                {rec.expected_memory_saving_bytes > 0
                  ? `-${(rec.expected_memory_saving_bytes / 1024).toFixed(0)} KB`
                  : "0 KB"}
              </td>
              <td style={{ fontSize: "0.85rem", color: "var(--text-muted)", maxWidth: "420px" }}>
                {rec.reason}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
