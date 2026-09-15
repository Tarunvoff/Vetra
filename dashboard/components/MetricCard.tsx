import React from "react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  change?: string;
  isPositive?: boolean;
  progressPercent?: number;
  progressColor?: string;
}

export function MetricCard({
  title,
  value,
  subtitle,
  change,
  isPositive,
  progressPercent,
  progressColor = "#00f2fe",
}: MetricCardProps) {
  return (
    <div className="glass-card" style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: "0.8rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>
          {title}
        </span>
        {change && (
          <span style={{ fontSize: "0.75rem", fontWeight: 700, color: isPositive ? "#10b981" : "#ef4444" }}>
            {change}
          </span>
        )}
      </div>

      <div style={{ fontSize: "1.75rem", fontWeight: 800, color: "#fff", letterSpacing: "-0.02em" }}>
        {value}
      </div>

      {subtitle && (
        <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
          {subtitle}
        </span>
      )}

      {progressPercent !== undefined && (
        <div style={{ marginTop: "0.5rem" }}>
          <div className="progress-bar-bg">
            <div
              className="progress-bar-fill"
              style={{
                width: `${Math.min(100, Math.max(0, progressPercent))}%`,
                background: progressColor,
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}
