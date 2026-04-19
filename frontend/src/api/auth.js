const TOKEN_KEY = "itbrain_access_token";

/*
  Save the JWT token in localStorage.

  Why localStorage for now:
  - simple for learning
  - easy to inspect in the browser
  - common for early SPA auth flows

  Later, for stricter security discussion, we can compare this
  with httpOnly cookie-based approaches.
*/
export function saveToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

/*
  Read the saved JWT token from localStorage.
*/
export function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

/*
  Remove the JWT token during logout.
*/
export function removeToken() {
    localStorage.removeItem(TOKEN_KEY);
}

/*
  Simple boolean helper for auth checks.
*/
export function isAuthenticated() {
    return Boolean(getToken());
}