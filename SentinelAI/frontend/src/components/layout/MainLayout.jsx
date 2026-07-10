import { Suspense, useState } from "react";
import { Outlet } from "react-router-dom";

import LoadingScreen from "../common/LoadingScreen.jsx";
import Navbar from "./Navbar.jsx";
import Sidebar from "./Sidebar.jsx";

export default function MainLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-950 dark:bg-slate-950 dark:text-white">
      <div className="flex min-h-screen">
        <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
        <div className="min-w-0 flex-1">
          <Navbar onMenuClick={() => setIsSidebarOpen(true)} />
          <main className="mx-auto w-full max-w-7xl px-4 py-6 lg:px-6">
            <Suspense fallback={<LoadingScreen />}>
              <Outlet />
            </Suspense>
          </main>
        </div>
      </div>
    </div>
  );
}
