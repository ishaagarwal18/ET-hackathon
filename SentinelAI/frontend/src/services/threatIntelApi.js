import { apiClient, unwrapApiResponse } from "./apiClient.js";

export async function sendThreatIntelQuestion(question) {
  const response = await apiClient.post("/chat/", {
    question,
    top_k: 5,
  });
  return unwrapApiResponse(response);
}
