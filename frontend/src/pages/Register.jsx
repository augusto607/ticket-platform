import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import PageContainer from "../components/layout/PageContainer";
import { useAuth } from "../context/AuthContext";

export default function Register() {
    const { register } = useAuth();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        full_name: "",
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
            await register(formData);
            navigate("/login");
        } catch (error) {
            console.error("Registration failed:", error);
            setErrorMessage("Registration failed. Please review your input.");
        }
    }

    return (
        <PageContainer>
            <h1 className="page-title">Register</h1>
            <p className="page-subtitle">
                Create an account to start managing your own tickets.
            </p>

            <Card>
                <form className="form-stack" onSubmit={handleSubmit}>
                    <Input
                        id="register-name"
                        name="full_name"
                        label="Full name"
                        type="text"
                        placeholder="Your full name"
                        value={formData.full_name}
                        onChange={handleChange}
                    />

                    <Input
                        id="register-email"
                        name="email"
                        label="Email"
                        type="email"
                        placeholder="you@example.com"
                        value={formData.email}
                        onChange={handleChange}
                    />

                    <Input
                        id="register-password"
                        name="password"
                        label="Password"
                        type="password"
                        placeholder="Choose a secure password"
                        value={formData.password}
                        onChange={handleChange}
                    />

                    {errorMessage && <p style={{ color: "var(--color-danger)" }}>{errorMessage}</p>}

                    <Button type="submit">Create account</Button>
                </form>
            </Card>
        </PageContainer>
    );
}