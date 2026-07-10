import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("sentinelai_access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export function unwrapApiResponse(response) {
  return response?.data?.data ?? response?.data;
}

export function normalizeApiError(error) {
  const payload = error?.response?.data;
  return {
    message: payload?.message || error?.message || "Request failed.",
    status: error?.response?.status || null,
    errors: payload?.errors || null,
    requestId: payload?.meta?.request_id || error?.response?.headers?.["x-request-id"] || null,
  };
}
