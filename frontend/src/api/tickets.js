import apiClient from "./client";

/*
  Fetch the authenticated user's tickets.
*/
export async function fetchMyTickets() {
  const response = await apiClient.get("/tickets/");
  return response.data;
}

/*
  Create a new ticket for the authenticated user.
*/
export async function createTicket(ticketData) {
  const response = await apiClient.post("/tickets/", ticketData);
  return response.data;
}

/*
  Update an existing ticket.

  ticketId: the ticket ID
  ticketData: only the fields we want to update
*/
export async function updateTicket(ticketId, ticketData) {
  const response = await apiClient.put(`/tickets/${ticketId}`, ticketData);
  return response.data;
}

/*
  Delete an existing ticket.
*/
export async function deleteTicket(ticketId) {
  await apiClient.delete(`/tickets/${ticketId}`);
}