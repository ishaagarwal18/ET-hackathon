/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        slatepanel: "#111827",
        cyber: {
          blue: "#2563eb",
          cyan: "#06b6d4",
          green: "#10b981",
          amber: "#f59e0b",
          red: "#ef4444",
        },
      },
      boxShadow: {
        soft: "0 18px 50px rgba(15, 23, 42, 0.12)",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
