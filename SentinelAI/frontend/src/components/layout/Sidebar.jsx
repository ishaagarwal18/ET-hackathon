import {
  AlertTriangle,
  BarChart3,
  Bot,
  FileText,
  LayoutDashboard,
  MonitorSmartphone,
  Network,
  Settings,
  ShieldAlert,
  ShieldCheck,
  Swords,
} from "lucide-react";
import { NavLink } from "react-router-dom";

import { cn } from "../../utils/cn.js";

const navItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Alerts", href: "/alerts", icon: AlertTriangle },
  { label: "Incidents", href: "/incidents", icon: ShieldAlert },
  { label: "Threat Intelligence", href: "/threat-intelligence", icon: Swords },
  { label: "SOC Assistant", href: "/soc-assistant", icon: Bot },
  { label: "Assets", href: "/assets", icon: MonitorSmartphone },
  { label: "Digital Twin", href: "/digital-twin", icon: Network },
  { label: "Reports", href: "/reports", icon: FileText },
  { label: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar({ isOpen, onClose }) {
  return (
    <>
      <div
        className={cn(
          "fixed inset-0 z-30 bg-slate-950/50 transition-opacity lg:hidden",
          isOpen ? "opacity-100" : "pointer-events-none opacity-0",
        )}
        onClick={onClose}
      />
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-72 border-r border-slate-200 bg-white transition-transform dark:border-slate-800 dark:bg-slate-950 lg:static lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="flex h-16 items-center gap-3 border-b border-slate-200 px-5 dark:border-slate-800">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-600 text-white">
            <ShieldCheck size={22} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-950 dark:text-white">SentinelAI</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">Cyber Resilience</p>
          </div>
        </div>

        <nav className="space-y-1 px-3 py-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.href}
                to={item.href}
                onClick={onClose}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition",
                    isActive
                      ? "bg-blue-600 text-white shadow-sm"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-900 dark:hover:text-white",
                  )
                }
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        <div className="absolute bottom-4 left-3 right-3 rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-slate-900 dark:text-white">
            <BarChart3 size={17} />
            Resilience Index
          </div>
          <div className="h-2 rounded-full bg-slate-100 dark:bg-slate-800">
            <div className="h-2 w-[72%] rounded-full bg-emerald-500" />
          </div>
          <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">72 percent operational readiness</p>
        </div>
      </aside>
    </>
  );
}
