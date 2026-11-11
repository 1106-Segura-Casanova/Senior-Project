// Purpose: Unit test or the frontend API

import {
    describe,
    it,
    expect,
    vi,
    afterEach
} from "vitest";

import {
    getMessages,
    createMessage,
    updateMessage,
    getCurrentProfile
} from "../services/api";

describe("API Service", () => {
    afterEach(() => {
        vi.restoreAllMocks();
    });

    it("retrieves messages using the authentication token", async () => {
        const mockMessages = [
            { id: 1, content: "Test message" }
        ];

        vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
            ok: true,
            json: vi.fn().mockResolvedValue(mockMessages)
        }));

        const result = await getMessages("test-token");

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/api/messages/",
            {
                headers: {
                    Authorization: "Bearer test-token"
                }
            }
        );

        expect(result).toEqual(mockMessages);
    });

    it("creates a message with authentication", async () => {
        const mockMessage = {
            id: 1,
            content: "New message"
        };

        vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
            ok: true,
            json: vi.fn().mockResolvedValue(mockMessage)
        }));

        const result = await createMessage(
            "New message",
            "test-token"
        );

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/api/messages/",
            {
                method: "POST",
                headers: {
                    Authorization: "Bearer test-token",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    content: "New message"
                })
            }
        );

        expect(result).toEqual(mockMessage);
    });

    it("updates a message using its ID and authentication token", async () => {
        const mockMessage = {
            id: 5,
            content: "Updated message"
        };

        vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
            ok: true,
            json: vi.fn().mockResolvedValue(mockMessage)
        }));

        const result = await updateMessage(
            5,
            "Updated message",
            "test-token"
        );

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/api/messages/5",
            {
                method: "PUT",
                headers: {
                    Authorization: "Bearer test-token",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    content: "Updated message"
                })
            }
        );

        expect(result).toEqual(mockMessage);
    });

    it("retrieves the current user's profile", async () => {
        const mockProfile = {
            id: 1,
            email: "test@example.com"
        };

        vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
            ok: true,
            json: vi.fn().mockResolvedValue(mockProfile)
        }));

        const result = await getCurrentProfile("test-token");

        expect(fetch).toHaveBeenCalledWith(
            "http://localhost:8000/api/auth/me",
            {
                method: "GET",
                headers: {
                    Authorization: "Bearer test-token"
                }
            }
        );

        expect(result).toEqual(mockProfile);
    });

    it("rejects requests without an authentication token", async () => {
        await expect(getMessages()).rejects.toThrow(
            "Authentication token is required."
        );

        expect(fetch).not.toHaveBeenCalled();
    });

    it("handles failed message retrieval", async () => {
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
            ok: false
        }));

        await expect(
            getMessages("test-token")
        ).rejects.toThrow("Failed to retrieve messages");
    });

    it("handles API errors when retrieving the user profile", async () => {
        vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
            ok: false,
            json: vi.fn().mockResolvedValue({
                detail: "Invalid or expired authentication token"
            })
        }));

        await expect(
            getCurrentProfile("test-token")
        ).rejects.toThrow(
            "Invalid or expired authentication token"
        );
    });

});
