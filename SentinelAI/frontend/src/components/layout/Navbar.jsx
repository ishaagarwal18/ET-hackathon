import { Bell, Menu, Moon, Search, Sun } from "lucide-react";

import { useNotifications } from "../../app/useNotifications.js";
import { useTheme } from "../../app/useTheme.js";

export default function Navbar({ onMenuClick }) {
  const { isDark, toggleTheme } = useTheme();
  const { notify } = useNotifications();

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between border-b border-slate-200 bg-white/90 px-4 backdrop-blur dark:border-slate-800 dark:bg-slate-950/90 lg:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          aria-label="Open navigation"
          onClick={onMenuClick}
          className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-900 dark:hover:text-white lg:hidden"
        >
          <Menu size={20} />
        </button>
        <div className="hidden min-w-72 items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 dark:border-slate-800 dark:bg-slate-900 md:flex">
          <Search size={16} className="text-slate-400" />
          <input
            aria-label="Search"
            placeholder="Search alerts, assets, incidents"
            className="w-full bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400 dark:text-white"
          />
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          aria-label="Toggle dark mode"
          onClick={toggleTheme}
          className="rounded-lg border border-slate-200 p-2 text-slate-600 transition hover:bg-slate-100 dark:border-slate-800 dark:text-slate-300 dark:hover:bg-slate-900"
        >
          {isDark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button
          type="button"
          aria-label="Create notification preview"
          onClick={() =>
            notify({
              title: "Analyst note queued",
              message: "A UI-only notification was added locally.",
              type: "info",
            })
          }
          className="relative rounded-lg border border-slate-200 p-2 text-slate-600 transition hover:bg-slate-100 dark:border-slate-800 dark:text-slate-300 dark:hover:bg-slate-900"
        >
          <Bell size={18} />
          <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500" />
        </button>
        <div className="ml-2 flex items-center gap-3 rounded-lg px-2 py-1.5">
          <div className="h-9 w-9 rounded-lg bg-slate-900 text-center text-sm font-semibold leading-9 text-white dark:bg-white dark:text-slate-950">
            SA
          </div>
          <div className="hidden text-sm sm:block">
            <p className="font-semibold text-slate-900 dark:text-white">Security Analyst</p>
            <p className="text-xs text-slate-500 dark:text-slate-400">SOC Command</p>
          </div>
        </div>
      </div>
    </header>
  );
}
