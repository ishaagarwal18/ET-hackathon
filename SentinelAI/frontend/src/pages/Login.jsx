import { useState } from "react";
import { LockKeyhole, ShieldCheck } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { apiClient, unwrapApiResponse } from "../services/apiClient.js";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      const response = await apiClient.post("/auth/login/", {
        username,
        password,
      });
      const data = unwrapApiResponse(response);
      localStorage.setItem("sentinelai_access_token", data.access);
      localStorage.setItem("sentinelai_refresh_token", data.refresh);
      localStorage.setItem("sentinelai_user", JSON.stringify(data.user));
      navigate("/dashboard");
    } catch {
      setError("Unable to sign in. Check credentials or backend availability.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="grid min-h-screen bg-slate-950 text-white lg:grid-cols-[1.05fr_0.95fr]">
      <section className="flex flex-col justify-between px-6 py-8 lg:px-12">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-600">
            <ShieldCheck size={24} />
          </div>
          <div>
            <p className="font-semibold">SentinelAI</p>
            <p className="text-sm text-slate-400">Cyber Resilience Platform</p>
          </div>
        </div>

        <div className="max-w-2xl py-16">
          <p className="text-sm font-semibold uppercase text-cyan-300">Secure SOC Access</p>
          <h1 className="mt-4 text-4xl font-semibold leading-tight md:text-6xl">Unified visibility for modern security teams.</h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-slate-300">
            Monitor alerts, incidents, assets, reports, and threat intelligence from a connected analyst workspace.
          </p>
        </div>

        <p className="text-sm text-slate-500">JWT authentication connected to the SentinelAI backend.</p>
      </section>

      <section className="flex items-center justify-center bg-white px-6 py-10 text-slate-950 dark:bg-slate-900 dark:text-white">
        <div className="w-full max-w-md rounded-lg border border-slate-200 p-6 shadow-soft dark:border-slate-800">
          <div className="mb-6">
            <LockKeyhole className="mb-3 text-blue-600" size={28} />
            <h2 className="text-xl font-semibold">Sign in</h2>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Use a backend account to access live dashboard data.</p>
          </div>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <label className="block">
              <span className="text-sm font-medium">Username</span>
              <input
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 outline-none transition focus:border-blue-500 dark:border-slate-800 dark:bg-slate-950"
                placeholder="soc_analyst"
                autoComplete="username"
              />
            </label>
            <label className="block">
              <span className="text-sm font-medium">Password</span>
              <input
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 outline-none transition focus:border-blue-500 dark:border-slate-800 dark:bg-slate-950"
                type="password"
                placeholder="Password"
                autoComplete="current-password"
              />
            </label>
            {error && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-200">{error}</p>}
            <button
              type="submit"
              disabled={isSubmitting}
              className="block w-full rounded-lg bg-blue-600 px-4 py-3 text-center text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? "Signing in..." : "Open Dashboard"}
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}
