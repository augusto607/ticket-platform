import axios from "axios";

/*
  Central Axios client for backend communication.

  Why this file matters:
  - keeps the backend base URL in one place
  - avoids repeating URLs everywhere
  - later we can inject auth tokens here
  - later we can add interceptors for 401 handling
*/
const apiClient = axios.create({
    baseURL: "http://localhost:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

export default apiClient;