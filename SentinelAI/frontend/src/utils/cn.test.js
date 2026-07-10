import { describe, expect, it } from "vitest";

import { cn } from "./cn.js";

describe("cn", () => {
  it("joins truthy class names and drops falsey values", () => {
    const disabledClass = false;

    expect(cn("base", disabledClass, "", null, undefined, "active")).toBe("base active");
  });
});
