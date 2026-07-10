import { motion } from "framer-motion";

import { cn } from "../../utils/cn.js";

export default function Card({ children, className = "", title, action }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.24 }}
      className={cn(
        "rounded-lg border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900",
        className,
      )}
    >
      {(title || action) && (
        <div className="mb-4 flex items-center justify-between gap-3">
          {title && <h2 className="text-sm font-semibold text-slate-900 dark:text-white">{title}</h2>}
          {action}
        </div>
      )}
      {children}
    </motion.section>
  );
}
