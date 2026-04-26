import apiClient from "./client";

/*
  Fetch the authenticated user's tickets.

  Because apiClient already injects the Bearer token,
  this request will automatically be authenticated.
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