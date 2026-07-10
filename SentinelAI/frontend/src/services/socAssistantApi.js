import { apiClient, unwrapApiResponse } from "./apiClient.js";

export async function sendSOCAssistantMessage({ message, context = {} }) {
  const response = await apiClient.post("/soc-assistant/chat/", {
    message,
    context,
  });
  return unwrapApiResponse(response);
}

export async function fetchSOCAssistantHistory() {
  const response = await apiClient.get("/soc-assistant/history/", {
    params: { limit: 25 },
  });
  return unwrapApiResponse(response);
}
