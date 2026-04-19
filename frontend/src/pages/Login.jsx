import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import PageContainer from "../components/layout/PageContainer";
import { useAuth } from "../context/AuthContext";

export default function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [errorMessage, setErrorMessage] = useState("");

    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");

        try {
            await login(formData);
            navigate("/tickets");
        } catch (error) {
            console.error("Login failed:", error);
            setErrorMessage("Login failed. Please verify your email and password.");
        }
    }

    return (
        <PageContainer>
            <h1 className="page-title">Login</h1>
            <p className="page-subtitle">
                Sign in to access your personal ticket workspace.
            </p>

            <Card>
                <form className="form-stack" onSubmit={handleSubmit}>
                    <Input
                        id="login-email"
                        name="email"
                        label="Email"
                        type="email"
                        placeholder="you@example.com"
                        value={formData.email}
                        onChange={handleChange}
                    />

                    <Input
                        id="login-password"
                        name="password"
                        label="Password"
                        type="password"
                        placeholder="Your password"
                        value={formData.password}
                        onChange={handleChange}
                    />

                    {errorMessage && <p style={{ color: "var(--color-danger)" }}>{errorMessage}</p>}

                    <Button type="submit">Login</Button>
                </form>
            </Card>
        </PageContainer>
    );
}