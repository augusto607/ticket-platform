import { Link } from "react-router-dom";

export default function Navbar() {
    return (
        <header className="topbar">
            <div className="topbar__inner">
                <div className="topbar__brand">Ticket Platform</div>

                <nav className="topbar__nav">
                    <Link className="topbar__link" to="/">
                        Dashboard
                    </Link>
                    <Link className="topbar__link" to="/tickets">
                        Tickets
                    </Link>
                    <Link className="topbar__link" to="/login">
                        Login
                    </Link>
                    <Link className="topbar__link" to="/register">
                        Register
                    </Link>
                </nav>
            </div>
        </header>
    );
}