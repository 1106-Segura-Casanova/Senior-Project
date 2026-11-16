// Purpose: Handle communication between frontend and backend
// rRecieved from Chatgpt
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function getAuthHeaders(token, includeContentType = false) {
    if (!token) {
        throw new Error("Authentication token is required.");
    }

    const headers = {
        Authorization: `Bearer ${token}`
    };

    if (includeContentType) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

export async function getMessages(token) {
    const response = await fetch(
        `${API_URL}/api/messages/`,
        {
            headers: getAuthHeaders(token)
        }
    );

    if (!response.ok) {
        throw new Error("Failed to retrieve messages");
    }

    return await response.json();
}

export async function createMessage(content, token) {
    const response = await fetch(
        `${API_URL}/api/messages/`,
        {
            method: "POST",
            headers: getAuthHeaders(token, true),
            body: JSON.stringify({ content })
        }
    );

    if (!response.ok) {
        throw new Error("Failed to create message");
    }

    return await response.json();
}

export async function updateMessage(id, content, token) {
    const response = await fetch(
        `${API_URL}/api/messages/${id}`,
        {
            method: "PUT",
            headers: getAuthHeaders(token, true),
            body: JSON.stringify({ content })
        }
    );

    if (!response.ok) {
        throw new Error("Failed to update message");
    }

    return await response.json();
}

export async function getCurrentProfile(token) {
    const response = await fetch(
        `${API_URL}/api/auth/me`,
        {
            method: "GET",
            headers: getAuthHeaders(token)
        }
    );

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        throw new Error(
            errorData.detail || "Failed to retrieve user profile"
        );
    }

    return await response.json();
}
