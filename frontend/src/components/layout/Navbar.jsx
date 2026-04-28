import { Link, useNavigate } from "react-router-dom";
import Button from "../ui/Button";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
    const { isAuthenticated, user, logout } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate("/login");
    }

    return (
        <header className="topbar">
            <div className="topbar__inner">
                <Link className="brand-logo" to="/">
                    <span className="brand-logo__mark">IT</span>
                    <span className="brand-logo__text">
                        <strong>Brain</strong>
                        <small>Platform</small>
                    </span>
                </Link>

                <nav className="topbar__nav">
                    <Link className="topbar__link" to="/">
                        Dashboard
                    </Link>

                    {isAuthenticated && (
                        <Link className="topbar__link" to="/tickets">
                            Tickets
                        </Link>
                    )}

                    {!isAuthenticated && (
                        <>
                            <Link className="topbar__link" to="/login">
                                Login
                            </Link>
                            <Link className="topbar__link" to="/register">
                                Register
                            </Link>
                        </>
                    )}

                    {isAuthenticated && (
                        <>
                            <span className="topbar__link">
                                {user?.full_name || user?.email}
                            </span>
                            <Button variant="secondary" onClick={handleLogout}>
                                Logout
                            </Button>
                        </>
                    )}
                </nav>
            </div>
        </header>
    );
}