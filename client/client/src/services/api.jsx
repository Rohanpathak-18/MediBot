import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "https://medibot-xuy1.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const sendMessage = async (message) => {
  const response = await api.post("/api/chat", {
    message,
  });

  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get("/api/health");

  return response.data;
};

export default api;