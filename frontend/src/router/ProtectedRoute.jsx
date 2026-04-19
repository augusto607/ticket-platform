import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/*
  Protect routes that should only be accessible to authenticated users.
*/
export default function ProtectedRoute({ children }) {
    const { isAuthenticated, isLoading } = useAuth();

    /*
      While auth state is loading, avoid redirecting too early.
    */
    if (isLoading) {
        return <div className="page-container">Loading session...</div>;
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
}