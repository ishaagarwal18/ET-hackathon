import { Bell, Lock, Moon, Shield } from "lucide-react";

import { useTheme } from "../app/useTheme.js";
import Card from "../components/common/Card.jsx";

const settings = [
  { title: "Role-based access controls", description: "Prepare granular permissions for SOC, GRC, and executive users.", icon: Lock },
  { title: "Security notifications", description: "Tune analyst notification channels and escalation behavior.", icon: Bell },
  { title: "Platform hardening", description: "Centralize secure defaults for sessions, audit logs, and data handling.", icon: Shield },
];

export default function Settings() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Workspace Controls</p>
        <h1 className="mt-1 text-2xl font-semibold">Settings</h1>
      </div>

      <Card title="Appearance">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-slate-100 p-3 text-slate-700 dark:bg-slate-800 dark:text-slate-200">
              <Moon size={20} />
            </div>
            <div>
              <p className="font-semibold text-slate-900 dark:text-white">Dark mode</p>
              <p className="text-sm text-slate-500 dark:text-slate-400">Switch the analyst workspace theme.</p>
            </div>
          </div>
          <button
            type="button"
            onClick={toggleTheme}
            className="relative h-8 w-14 rounded-full bg-slate-200 transition dark:bg-blue-600"
            aria-label="Toggle dark mode"
          >
            <span className={`absolute top-1 h-6 w-6 rounded-full bg-white shadow transition ${isDark ? "left-7" : "left-1"}`} />
          </button>
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-3">
        {settings.map((setting) => {
          const Icon = setting.icon;
          return (
            <Card key={setting.title}>
              <Icon className="text-blue-600 dark:text-blue-400" size={24} />
              <h2 className="mt-4 text-base font-semibold text-slate-900 dark:text-white">{setting.title}</h2>
              <p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">{setting.description}</p>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
