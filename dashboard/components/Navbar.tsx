"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield, Activity, Cpu, Layers, DollarSign, BarChart3 } from "lucide-react";

export function Navbar({ isSimulated = true }: { isSimulated?: boolean }) {
  const pathname = usePathname();

  const navLinks = [
    { href: "/", label: "Overview", icon: Activity },
    { href: "/cache", label: "KV Cache", icon: Layers },
    { href: "/recommendations", label: "Recommendations", icon: Cpu },
    { href: "/benchmarks", label: "Benchmarks", icon: BarChart3 },
    { href: "/security", label: "Security", icon: Shield },
    { href: "/optimization", label: "Economics", icon: DollarSign },
  ];

  return (
    <header style={{ borderBottom: "1px solid var(--border-color)", background: "rgba(17, 23, 38, 0.9)", backdropFilter: "blur(12px)", position: "sticky", top: 0, zIndex: 50 }}>
      <div style={{ maxWidth: "1400px", margin: "0 auto", padding: "1rem 2rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "2rem" }}>
          <Link href="/" style={{ display: "flex", alignItems: "center", gap: "0.75rem", textDecoration: "none", color: "inherit" }}>
            <div style={{ background: "linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)", padding: "0.5rem", borderRadius: "8px", display: "flex" }}>
              <Shield size={22} color="#0a0d14" />
            </div>
            <div>
              <span style={{ fontSize: "1.25rem", fontWeight: 800, color: "#00f2fe", letterSpacing: "-0.025em" }}>Vetra</span>
              <span style={{ fontSize: "0.7rem", color: "var(--text-muted)", marginLeft: "0.5rem", textTransform: "uppercase" }}>Control Plane</span>
            </div>
          </Link>

          <nav style={{ display: "flex", gap: "0.5rem" }}>
            {navLinks.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "0.4rem",
                    padding: "0.5rem 0.85rem",
                    borderRadius: "6px",
                    fontSize: "0.875rem",
                    fontWeight: 500,
                    textDecoration: "none",
                    color: isActive ? "#00f2fe" : "var(--text-muted)",
                    background: isActive ? "rgba(0, 242, 254, 0.1)" : "transparent",
                    transition: "all 0.15s ease",
                  }}
                >
                  <Icon size={16} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
          <div className={isSimulated ? "badge badge-sim" : "badge badge-live"}>
            <span style={{ display: "inline-block", width: "6px", height: "6px", borderRadius: "50%", background: isSimulated ? "#f59e0b" : "#10b981" }}></span>
            {isSimulated ? "SIMULATION MODE" : "LIVE CLUSTER"}
          </div>
          <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Engine: vLLM 0.4.x+</span>
        </div>
      </div>
    </header>
  );
}
