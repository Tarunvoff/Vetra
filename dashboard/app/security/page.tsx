import { MetricCard } from "@/components/MetricCard";

export const dynamic = "force-dynamic";

export default function SecurityPage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "2rem" }}>
      <div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>Multi-Tenant Security & Isolation</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: "0.25rem" }}>
          Phase 2 architecture for tenant boundaries, ACLs, TTL governance, and audit trails.
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "1.25rem" }}>
        <MetricCard
          title="Isolation Boundary"
          value="Strict Zero-Cross"
          subtitle="Cross-tenant cache sharing blocked by default"
        />
        <MetricCard
          title="Active Namespaces"
          value="3 Registered"
          subtitle="Tenant A, Tenant B, System Public"
        />
        <MetricCard
          title="Security Violations"
          value="0 Blocked"
          subtitle="100% authorization compliance"
          isPositive={true}
        />
      </div>

      <div className="glass-card">
        <h3 style={{ fontSize: "1.1rem", fontWeight: 700, marginBottom: "1rem" }}>Tenant Policy Configurations</h3>
        <table>
          <thead>
            <tr>
              <th>Tenant ID</th>
              <th>Allowed Namespaces</th>
              <th>Cross-Tenant Reuse</th>
              <th>TTL Limit</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ fontWeight: 600, color: "#00f2fe" }}>tenant_alpha</td>
              <td>["default", "alpha_private"]</td>
              <td><span className="badge badge-evict">DENIED</span></td>
              <td>3600s</td>
              <td><span className="badge badge-live">Active</span></td>
            </tr>
            <tr>
              <td style={{ fontWeight: 600, color: "#4facfe" }}>tenant_beta</td>
              <td>["default", "beta_private"]</td>
              <td><span className="badge badge-evict">DENIED</span></td>
              <td>3600s</td>
              <td><span className="badge badge-live">Active</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
