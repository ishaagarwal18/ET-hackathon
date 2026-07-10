import { beforeEach, describe, expect, it } from "vitest";

import { apiClient, normalizeApiError, unwrapApiResponse } from "./apiClient.js";

describe("apiClient", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("adds bearer token from local storage", async () => {
    localStorage.setItem("sentinelai_access_token", "token-123");

    const config = await apiClient.interceptors.request.handlers[0].fulfilled({ headers: {} });

    expect(config.headers.Authorization).toBe("Bearer token-123");
  });

  it("unwraps standardized API responses", () => {
    expect(unwrapApiResponse({ data: { data: { status: "healthy" } } })).toEqual({ status: "healthy" });
    expect(unwrapApiResponse({ data: { raw: true } })).toEqual({ raw: true });
  });

  it("normalizes backend error envelopes", () => {
    const normalized = normalizeApiError({
      response: {
        status: 403,
        headers: { "x-request-id": "req-123" },
        data: {
          message: "Permission denied.",
          errors: { detail: "Forbidden" },
          meta: { request_id: "req-456" },
        },
      },
    });

    expect(normalized).toEqual({
      message: "Permission denied.",
      status: 403,
      errors: { detail: "Forbidden" },
      requestId: "req-456",
    });
  });
});
