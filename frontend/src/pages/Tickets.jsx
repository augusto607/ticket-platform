import { useEffect, useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import PageContainer from "../components/layout/PageContainer";
import { useAuth } from "../context/AuthContext";
import { createTicket, fetchMyTickets } from "../api/tickets";

export default function Tickets() {
    const { user } = useAuth();

    const [tickets, setTickets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        priority: "medium",
    });

    /*
      Load the authenticated user's tickets from the backend.
    */
    async function loadTickets() {
        setIsLoading(true);
        setErrorMessage("");

        try {
            const data = await fetchMyTickets();
            setTickets(data);
        } catch (error) {
            console.error("Failed to load tickets:", error);
            setErrorMessage("Could not load your tickets. Please try again.");
        } finally {
            setIsLoading(false);
        }
    }

    /*
      Load tickets once when the page mounts.
    */
    useEffect(() => {
        loadTickets();
    }, []);

    /*
      Update local form state when the user types.
    */
    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    /*
      Submit a new ticket to the backend and refresh the list.
    */
    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");
        setSuccessMessage("");
        setIsSubmitting(true);

        try {
            const newTicket = await createTicket(formData);

            /*
              Optimistic UI update:
              add the new ticket to the top of the list immediately
              instead of waiting for a full refetch.
            */
            setTickets((previous) => [newTicket, ...previous]);

            setFormData({
                title: "",
                description: "",
                priority: "medium",
            });

            setSuccessMessage("Ticket created successfully.");
        } catch (error) {
            console.error("Failed to create ticket:", error);
            setErrorMessage("Could not create the ticket. Please review your input.");
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <PageContainer>
            <h1 className="page-title">My Tickets</h1>
            <p className="page-subtitle">
                Welcome {user?.full_name || user?.email}. Here you can create and view
                your own tickets in the platform.
            </p>

            <div className="section-stack">
                <Card>
                    <h2>Create a new ticket</h2>

                    <form className="form-stack" onSubmit={handleSubmit}>
                        <Input
                            id="ticket-title"
                            name="title"
                            label="Title"
                            type="text"
                            placeholder="Short summary of the issue"
                            value={formData.title}
                            onChange={handleChange}
                        />

                        <Input
                            id="ticket-description"
                            name="description"
                            label="Description"
                            type="text"
                            placeholder="Describe the issue or request"
                            value={formData.description}
                            onChange={handleChange}
                        />

                        <div className="ui-input-wrapper">
                            <label className="ui-input-label" htmlFor="ticket-priority">
                                Priority
                            </label>
                            <select
                                id="ticket-priority"
                                name="priority"
                                className="ui-input"
                                value={formData.priority}
                                onChange={handleChange}
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                            </select>
                        </div>

                        {errorMessage && (
                            <p className="feedback-message feedback-message--error">
                                {errorMessage}
                            </p>
                        )}

                        {successMessage && (
                            <p className="feedback-message feedback-message--success">
                                {successMessage}
                            </p>
                        )}

                        <Button type="submit" disabled={isSubmitting}>
                            {isSubmitting ? "Creating..." : "Create Ticket"}
                        </Button>
                    </form>
                </Card>

                <Card>
                    <div className="ticket-card__header">
                        <div>
                            <h2 style={{ margin: 0 }}>My ticket list</h2>
                            <p className="page-subtitle" style={{ margin: "8px 0 0" }}>
                                Your authenticated tickets are loaded directly from the backend.
                            </p>
                        </div>

                        <Button variant="secondary" onClick={loadTickets}>
                            Refresh
                        </Button>
                    </div>

                    {isLoading ? (
                        <p>Loading tickets...</p>
                    ) : tickets.length === 0 ? (
                        <p>You do not have any tickets yet.</p>
                    ) : (
                        <div className="ticket-list">
                            {tickets.map((ticket) => (
                                <Card key={ticket.id}>
                                    <div className="ticket-card__header">
                                        <div>
                                            <h3 className="ticket-card__title">{ticket.title}</h3>
                                            <p style={{ margin: "8px 0 0", color: "var(--color-text-soft)" }}>
                                                {ticket.description || "No description provided."}
                                            </p>
                                        </div>
                                        <div className="ticket-badge">#{ticket.id}</div>
                                    </div>

                                    <div className="ticket-card__meta">
                                        <span className="ticket-badge ticket-badge--status">
                                            Status: {ticket.status}
                                        </span>
                                        <span className="ticket-badge ticket-badge--priority">
                                            Priority: {ticket.priority}
                                        </span>
                                        <span className="ticket-badge">
                                            Created: {new Date(ticket.created_at).toLocaleString()}
                                        </span>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    )}
                </Card>
            </div>
        </PageContainer>
    );
}