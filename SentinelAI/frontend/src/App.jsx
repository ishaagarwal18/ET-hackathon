import { BrowserRouter } from "react-router-dom";

import { NotificationProvider } from "./app/NotificationContext.jsx";
import { ThemeProvider } from "./app/ThemeContext.jsx";
import AppRoutes from "./routes/AppRoutes.jsx";

export default function App() {
  return (
    <ThemeProvider>
      <NotificationProvider>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </NotificationProvider>
    </ThemeProvider>
  );
}
