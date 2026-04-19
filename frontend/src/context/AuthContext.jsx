import { createContext, useContext, useEffect, useState } from "react";
import apiClient from "../api/client";
import { getToken, removeToken, saveToken } from "../api/auth";

const AuthContext = createContext(null);

/*
  Custom hook to consume auth state from anywhere in the app.
*/
export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    /*
      Load the current user on app startup if a token exists.
      This keeps the session alive across browser refreshes.
    */
    useEffect(() => {
        async function loadCurrentUser() {
            const token = getToken();

            if (!token) {
                setIsLoading(false);
                return;
            }

            try {
                const response = await apiClient.get("/auth/me");
                setUser(response.data);
            } catch (error) {
                console.error("Failed to load current user:", error);
                removeToken();
                setUser(null);
            } finally {
                setIsLoading(false);
            }
        }

        loadCurrentUser();
    }, []);

    /*
      Register a new user in the backend.
    */
    async function register({ email, full_name, password }) {
        const response = await apiClient.post("/auth/register", {
            email,
            full_name,
            password,
        });

        return response.data;
    }

    /*
      Log in using OAuth2-style form data.
  
      Important:
      the backend expects x-www-form-urlencoded with:
      - username
      - password
  
      In this project, username = email.
    */
    async function login({ email, password }) {
        const formData = new URLSearchParams();
        formData.append("username", email);
        formData.append("password", password);

        const tokenResponse = await apiClient.post("/auth/login", formData, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        const accessToken = tokenResponse.data.access_token;
        saveToken(accessToken);

        const userResponse = await apiClient.get("/auth/me");
        setUser(userResponse.data);

        return userResponse.data;
    }

    /*
      Clear local auth state and remove the saved token.
    */
    function logout() {
        removeToken();
        setUser(null);
    }

    const value = {
        user,
        isLoading,
        isAuthenticated: Boolean(user),
        register,
        login,
        logout,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}