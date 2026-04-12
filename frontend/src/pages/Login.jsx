import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import PageContainer from "../components/layout/PageContainer";

export default function Login() {
    return (
        <PageContainer>
            <h1 className="page-title">Login</h1>
            <p className="page-subtitle">
                Sign in to access your personal ticket workspace.
            </p>

            <Card>
                <form className="form-stack">
                    <Input
                        id="login-email"
                        label="Email"
                        type="email"
                        placeholder="you@example.com"
                    />
                    <Input
                        id="login-password"
                        label="Password"
                        type="password"
                        placeholder="Your password"
                    />
                    <Button type="submit">Login</Button>
                </form>
            </Card>
        </PageContainer>
    );
}