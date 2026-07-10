import { ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

export default function LoadingScreen() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
      <motion.div
        animate={{ scale: [1, 1.04, 1], opacity: [0.82, 1, 0.82] }}
        transition={{ duration: 1.4, repeat: Infinity }}
        className="flex items-center gap-3"
      >
        <ShieldCheck className="text-cyan-300" size={34} />
        <span className="text-lg font-semibold tracking-wide">SentinelAI</span>
      </motion.div>
    </div>
  );
}
