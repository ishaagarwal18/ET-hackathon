import { Navigate, Route, Routes } from "react-router-dom";

import MainLayout from "../components/layout/MainLayout.jsx";
import Alerts from "../pages/Alerts.jsx";
import Assets from "../pages/Assets.jsx";
import CyberDigitalTwin from "../pages/CyberDigitalTwin.jsx";
import Dashboard from "../pages/Dashboard.jsx";
import Incidents from "../pages/Incidents.jsx";
import Login from "../pages/Login.jsx";
import Reports from "../pages/Reports.jsx";
import Settings from "../pages/Settings.jsx";
import SOCAssistant from "../pages/SOCAssistant.jsx";
import ThreatIntelligence from "../pages/ThreatIntelligence.jsx";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/incidents" element={<Incidents />} />
        <Route path="/threat-intelligence" element={<ThreatIntelligence />} />
        <Route path="/soc-assistant" element={<SOCAssistant />} />
        <Route path="/assets" element={<Assets />} />
        <Route path="/digital-twin" element={<CyberDigitalTwin />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
