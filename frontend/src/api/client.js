import axios from "axios";
import { getToken } from "./auth";

/*
  Central Axios client for backend communication.

  We keep backend base URL and default JSON headers here.
  We also attach the JWT token automatically when available.
*/
const apiClient = axios.create({
    baseURL: "http://localhost:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

/*
  Request interceptor:
  before each request, if a token exists, attach it as
  Authorization: Bearer <token>
*/
apiClient.interceptors.request.use((config) => {
    const token = getToken();

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

export default apiClient;