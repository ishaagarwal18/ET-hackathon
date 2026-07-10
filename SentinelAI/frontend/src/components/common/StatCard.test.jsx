import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import StatCard from "./StatCard.jsx";

vi.mock("framer-motion", () => ({
  motion: {
    section: ({ children, ...props }) => <section {...props}>{children}</section>,
  },
}));

describe("StatCard", () => {
  it("renders metric content and positive trend indicator", () => {
    render(<StatCard label="Active Alerts" value="42" change="+12%" tone="red" />);

    expect(screen.getByText("Active Alerts")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
    expect(screen.getByText("+12%")).toBeInTheDocument();
  });

  it("renders negative trend values without throwing", () => {
    render(<StatCard label="Risk Score" value="68" change="-4%" tone="green" />);

    expect(screen.getByText("-4%")).toBeInTheDocument();
  });
});
