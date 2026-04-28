import { useEffect, useState } from "react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Input from "../components/ui/Input";
import PageContainer from "../components/layout/PageContainer";
import { useAuth } from "../context/AuthContext";
import {
    createTicket,
    deleteTicket,
    fetchMyTickets,
    updateTicket,
} from "../api/tickets";

export default function Tickets() {
    const { user } = useAuth();

    const [tickets, setTickets] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [actionTicketId, setActionTicketId] = useState(null);

    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const [formData, setFormData] = useState({
        title: "",
        description: "",
        priority: "medium",
    });

    const [ticketPendingDelete, setTicketPendingDelete] = useState(null);

    /*
      Load tickets from the backend for the authenticated user.
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

    useEffect(() => {
        loadTickets();
    }, []);

    /*
      Generic form change handler for ticket creation form.
    */
    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((previous) => ({
            ...previous,
            [name]: value,
        }));
    }

    /*
      Create a new ticket.
    */
    async function handleSubmit(event) {
        event.preventDefault();
        setErrorMessage("");
        setSuccessMessage("");
        setIsSubmitting(true);

        try {
            const newTicket = await createTicket(formData);

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

    /*
      Update one ticket field, such as status or priority.
    */
    async function handleTicketUpdate(ticketId, updateData) {
        setErrorMessage("");
        setSuccessMessage("");
        setActionTicketId(ticketId);

        try {
            const updatedTicket = await updateTicket(ticketId, updateData);

            setTickets((previous) =>
                previous.map((ticket) =>
                    ticket.id === ticketId ? updatedTicket : ticket
                )
            );

            setSuccessMessage("Ticket updated successfully.");
        } catch (error) {
            console.error("Failed to update ticket:", error);
            setErrorMessage("Could not update the ticket. Please try again.");
        } finally {
            setActionTicketId(null);
        }
    }

    /*
      Delete one ticket after user confirmation.
    */
    async function handleTicketDelete(ticketId) {
        setErrorMessage("");
        setSuccessMessage("");
        setActionTicketId(ticketId);

        try {
            await deleteTicket(ticketId);

            setTickets((previous) =>
                previous.filter((ticket) => ticket.id !== ticketId)
            );

            setTicketPendingDelete(null);
            setSuccessMessage("Ticket deleted successfully.");
        } catch (error) {
            console.error("Failed to delete ticket:", error);
            setErrorMessage("Could not delete the ticket. Please try again.");
        } finally {
            setActionTicketId(null);
        }
    }

    return (
        <PageContainer>
            <h1 className="page-title">My Tickets</h1>
            <p className="page-subtitle">
                Welcome {user?.full_name || user?.email}. Create, review, and manage
                your own tickets.
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
                                Manage tickets loaded from the protected backend API.
                            </p>
                        </div>

                        <Button variant="secondary" onClick={loadTickets}>
                            Refresh
                        </Button>
                    </div>

                    {isLoading ? (
                        <p>Loading tickets...</p>
                    ) : tickets.length === 0 ? (
                        <div className="empty-state">
                            <p>You do not have any tickets yet.</p>
                            <p>Create your first ticket using the form above.</p>
                        </div>
                    ) : (
                        <div className="ticket-list">
                            {tickets.map((ticket) => (
                                <Card key={ticket.id}>
                                    <div className="ticket-card__header">
                                        <div>
                                            <h3 className="ticket-card__title">{ticket.title}</h3>
                                            <p
                                                style={{
                                                    margin: "8px 0 0",
                                                    color: "var(--color-text-soft)",
                                                }}
                                            >
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
                                        <span className="ticket-badge">
                                            Updated: {new Date(ticket.updated_at).toLocaleString()}
                                        </span>
                                    </div>

                                    <div className="ticket-actions">
                                        <div className="ticket-action-group">
                                            <label className="ticket-action-label">
                                                Update status
                                            </label>
                                            <select
                                                className="ui-input"
                                                value={ticket.status}
                                                disabled={actionTicketId === ticket.id}
                                                onChange={(event) =>
                                                    handleTicketUpdate(ticket.id, {
                                                        status: event.target.value,
                                                    })
                                                }
                                            >
                                                <option value="open">Open</option>
                                                <option value="in_progress">In progress</option>
                                                <option value="closed">Closed</option>
                                            </select>
                                        </div>

                                        <div className="ticket-action-group">
                                            <label className="ticket-action-label">
                                                Update priority
                                            </label>
                                            <select
                                                className="ui-input"
                                                value={ticket.priority}
                                                disabled={actionTicketId === ticket.id}
                                                onChange={(event) =>
                                                    handleTicketUpdate(ticket.id, {
                                                        priority: event.target.value,
                                                    })
                                                }
                                            >
                                                <option value="low">Low</option>
                                                <option value="medium">Medium</option>
                                                <option value="high">High</option>
                                            </select>
                                        </div>

                                        <div className="ticket-action-group">
                                            <label className="ticket-action-label">Danger zone</label>

                                            {ticketPendingDelete === ticket.id ? (
                                                <div className="delete-confirmation">
                                                    <p>Delete this ticket?</p>

                                                    <div className="delete-confirmation__actions">
                                                        <Button
                                                            variant="danger"
                                                            disabled={actionTicketId === ticket.id}
                                                            onClick={() => handleTicketDelete(ticket.id)}
                                                        >
                                                            Yes, delete
                                                        </Button>

                                                        <Button
                                                            variant="secondary"
                                                            disabled={actionTicketId === ticket.id}
                                                            onClick={() => setTicketPendingDelete(null)}
                                                        >
                                                            Cancel
                                                        </Button>
                                                    </div>
                                                </div>
                                            ) : (
                                                <Button
                                                    variant="danger"
                                                    disabled={actionTicketId === ticket.id}
                                                    onClick={() => setTicketPendingDelete(ticket.id)}
                                                >
                                                    Delete
                                                </Button>
                                            )}
                                        </div>
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