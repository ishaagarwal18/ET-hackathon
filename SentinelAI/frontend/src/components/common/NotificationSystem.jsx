import { AlertTriangle, CheckCircle2, Info, X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

const icons = {
  info: Info,
  success: CheckCircle2,
  warning: AlertTriangle,
};

export default function NotificationSystem({ notifications, onDismiss }) {
  return (
    <div className="pointer-events-none fixed right-4 top-4 z-50 flex w-[calc(100%-2rem)] max-w-sm flex-col gap-3">
      <AnimatePresence>
        {notifications.map((notification) => {
          const Icon = icons[notification.type] || Info;
          return (
            <motion.div
              key={notification.id}
              initial={{ opacity: 0, x: 24 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 24 }}
              className="pointer-events-auto rounded-lg border border-slate-200 bg-white p-4 shadow-soft dark:border-slate-800 dark:bg-slate-900"
            >
              <div className="flex gap-3">
                <Icon className="mt-0.5 text-amber-500" size={18} />
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold text-slate-900 dark:text-white">{notification.title}</p>
                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{notification.message}</p>
                </div>
                <button
                  type="button"
                  aria-label="Dismiss notification"
                  onClick={() => onDismiss(notification.id)}
                  className="rounded-md p-1 text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 dark:hover:bg-slate-800 dark:hover:text-slate-200"
                >
                  <X size={16} />
                </button>
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
