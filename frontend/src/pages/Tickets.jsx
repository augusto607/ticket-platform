import Card from "../components/ui/Card";
import PageContainer from "../components/layout/PageContainer";
import { useAuth } from "../context/AuthContext";

export default function Tickets() {
    const { user } = useAuth();

    return (
        <PageContainer>
            <h1 className="page-title">My Tickets</h1>
            <p className="page-subtitle">
                Welcome {user?.full_name || user?.email}. This area will soon display
                your real ticket list and ticket creation workflow.
            </p>

            <Card>
                <p>
                    Authentication is already connected. The next step is to load your
                    real ticket data from the backend.
                </p>
            </Card>
        </PageContainer>
    );
}