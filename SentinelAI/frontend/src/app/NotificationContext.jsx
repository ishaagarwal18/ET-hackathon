import { useCallback, useMemo, useState } from "react";

import NotificationSystem from "../components/common/NotificationSystem.jsx";
import { NotificationContext } from "./notificationContextValue.js";

export function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([
    {
      id: "initial-risk",
      title: "Risk posture updated",
      message: "Current platform risk is elevated across identity and cloud assets.",
      type: "warning",
    },
  ]);

  const dismiss = useCallback((id) => {
    setNotifications((items) => items.filter((item) => item.id !== id));
  }, []);

  const notify = useCallback((notification) => {
    const id = crypto.randomUUID();
    setNotifications((items) => [{ id, ...notification }, ...items].slice(0, 4));
  }, []);

  const value = useMemo(() => ({ notify, dismiss }), [notify, dismiss]);

  return (
    <NotificationContext.Provider value={value}>
      {children}
      <NotificationSystem notifications={notifications} onDismiss={dismiss} />
    </NotificationContext.Provider>
  );
}
