import Card from "../components/ui/Card";
import PageContainer from "../components/layout/PageContainer";

export default function Dashboard() {
    return (
        <PageContainer>
            <h1 className="page-title">Dashboard</h1>
            <p className="page-subtitle">
                Welcome to your ticket platform. This dashboard will evolve into the
                main workspace for authentication, ticket activity, and future platform
                modules.
            </p>

            <div className="grid-3">
                <Card>
                    <h3>Authentication</h3>
                    <p>Users can register, log in, and work with protected routes.</p>
                </Card>

                <Card>
                    <h3>Tickets</h3>
                    <p>Each user can create and manage only their own tickets.</p>
                </Card>

                <Card>
                    <h3>Roadmap</h3>
                    <p>Future versions will add roles, permissions, and CMDB features.</p>
                </Card>
            </div>
        </PageContainer>
    );
}