import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import PageContainer from "../components/layout/PageContainer";

export default function Register() {
    return (
        <PageContainer>
            <h1 className="page-title">Register</h1>
            <p className="page-subtitle">
                Create an account to start managing your own tickets.
            </p>

            <Card>
                <form className="form-stack">
                    <Input
                        id="register-name"
                        label="Full name"
                        type="text"
                        placeholder="Your full name"
                    />
                    <Input
                        id="register-email"
                        label="Email"
                        type="email"
                        placeholder="you@example.com"
                    />
                    <Input
                        id="register-password"
                        label="Password"
                        type="password"
                        placeholder="Choose a secure password"
                    />
                    <Button type="submit">Create account</Button>
                </form>
            </Card>
        </PageContainer>
    );
}