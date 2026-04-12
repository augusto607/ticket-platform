import Card from "../components/ui/Card";
import PageContainer from "../components/layout/PageContainer";

export default function Tickets() {
    return (
        <PageContainer>
            <h1 className="page-title">My Tickets</h1>
            <p className="page-subtitle">
                This area will display the authenticated user’s ticket list and ticket
                creation workflow.
            </p>

            <Card>
                <p>Ticket UI integration will be added in the next frontend step.</p>
            </Card>
        </PageContainer>
    );
}