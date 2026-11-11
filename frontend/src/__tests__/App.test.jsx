// Purpose: Unit Test for the react frontend

import {
    render,
    screen,
    fireEvent,
    waitFor
} from "@testing-library/react";

import {
    describe,
    it,
    expect,
    vi,
    beforeEach
} from "vitest";

import App from "../App";

import {
    subscribeToAuthChanges,
    getUserToken
} from "../services/auth";

import {
    getMessages,
    createMessage,
    getCurrentProfile
} from "../services/api";


// MOCK FIREBASE AUTHENTICATION

vi.mock("../services/auth", () => ({
    subscribeToAuthChanges: vi.fn(),

    registerUser: vi.fn(),

    loginUser: vi.fn(),

    logoutUser: vi.fn(),

    getUserToken: vi.fn()
}));


// MOCK API FUNCTIONS

vi.mock("../services/api", () => ({
    getMessages: vi.fn(),

    createMessage: vi.fn(),

    getCurrentProfile: vi.fn()
}));


describe("Jomini Library App", () => {

    beforeEach(() => {
        vi.clearAllMocks();

        subscribeToAuthChanges.mockImplementation((callback) => {
            callback(null);
            return vi.fn();
        });

        getUserToken.mockResolvedValue("test-firebase-token");

        getMessages.mockResolvedValue([]);

        createMessage.mockResolvedValue({
            id: 1,
            content: "Test message"
        });

        getCurrentProfile.mockResolvedValue({
            id: 1,
            email: "test@example.com",
            display_name: "Test User",
            firebase_uid: "test-firebase-uid",
            created_at: new Date().toISOString()
        });
    });


    it("renders the login interface when no user is authenticated", async () => {
        render(<App />);

        expect(
            screen.getByRole("heading", {
                name: "Jomini Library"
            })
        ).toBeInTheDocument();

        expect(
            await screen.findByRole("heading", {
                name: "Login"
            })
        ).toBeInTheDocument();

        expect(
            screen.getByPlaceholderText("Email address")
        ).toBeInTheDocument();

        expect(
            screen.getByPlaceholderText("Password")
        ).toBeInTheDocument();

        expect(
            screen.getByRole("button", {
                name: "Login"
            })
        ).toBeInTheDocument();

        expect(
            screen.getByRole("button", {
                name: "Need an account? Register"
            })
        ).toBeInTheDocument();
    });


    it("switches from Login to Register", async () => {
        render(<App />);

        await screen.findByRole("heading", {
            name: "Login"
        });

        fireEvent.click(
            screen.getByRole("button", {
                name: "Need an account? Register"
            })
        );

        expect(
            screen.getByRole("heading", {
                name: "Create Account"
            })
        ).toBeInTheDocument();
    });


    it("switches from Register back to Login", async () => {
        render(<App />);

        await screen.findByRole("heading", {
            name: "Login"
        });

        fireEvent.click(
            screen.getByRole("button", {
                name: "Need an account? Register"
            })
        );

        fireEvent.click(
            screen.getByRole("button", {
                name: "Already have an account? Login"
            })
        );

        expect(
            screen.getByRole("heading", {
                name: "Login"
            })
        ).toBeInTheDocument();
    });


    it("does not retrieve messages when no user is authenticated", async () => {
        render(<App />);

        await screen.findByRole("heading", {
            name: "Login"
        });

        expect(getMessages).not.toHaveBeenCalled();
    });


    it("retrieves messages using the authenticated user's token", async () => {
        const testUser = {
            uid: "test-firebase-uid",
            email: "test@example.com"
        };

        subscribeToAuthChanges.mockImplementation((callback) => {
            callback(testUser);
            return vi.fn();
        });

        render(<App />);

        await waitFor(() => {
            expect(getUserToken).toHaveBeenCalledWith(testUser);

            expect(getMessages).toHaveBeenCalledWith(
                "test-firebase-token"
            );
        });
    });

});
