// Purpose: Connects everythng together

import { useState, useEffect } from "react";

import {
    getMessages,
    createMessage,
    getCurrentProfile
} from "./services/api";

import {
    registerUser,
    loginUser,
    logoutUser,
    subscribeToAuthChanges,
    getUserToken
} from "./services/auth";

import "./App.css";

function App() {

    // -------------------------------
    // AUTHENTICATION STATE
    // -------------------------------

    const [user, setUser] = useState(null);

    const [authLoading, setAuthLoading] = useState(true);

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const [isRegistering, setIsRegistering] = useState(false);

    const [authError, setAuthError] = useState("");

    const [profile, setProfile] = useState(null);

    const [profileLoading, setProfileLoading] = useState(false);

    const [profileError, setProfileError] = useState("");


    // -------------------------------
    // MESSAGE STATE
    // -------------------------------

    const [messages, setMessages] = useState([]);

    const [content, setContent] = useState("");

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    // -------------------------------
    // MONITOR FIREBASE AUTHENTICATION
    // -------------------------------

    useEffect(() => {

        const unsubscribe = subscribeToAuthChanges((currentUser) => {

            setUser(currentUser);

            setAuthLoading(false);

        });

        return () => unsubscribe();

    }, []);

    // Retrieve the user's PostgreSQL profile after Firebase authentication
    useEffect(() => {

        if (!user) {
            setProfile(null);
            setProfileError("");
            return;
        }

        let cancelled = false;

        async function loadProfile() {

            setProfileLoading(true);
            setProfileError("");

            try {
                // Step 1: Obtain Firebase ID token
                const token = await getUserToken(user);

                // Step 2: Send token to FastAPI and retrieve PostgreSQL profile
                const data = await getCurrentProfile(token);

                if (!cancelled) {
                    setProfile(data);
                }

            } catch (err) {

                if (!cancelled) {
                    setProfileError(err.message);
                }

            } finally {

                if (!cancelled) {
                    setProfileLoading(false);
                }
            }
        }

        loadProfile();

        return () => {
            cancelled = true;
        };

    }, [user]);


    // -------------------------------
    // REGISTER OR LOGIN
    // -------------------------------

    async function handleAuthSubmit(event) {

        event.preventDefault();

        setAuthError("");

        try {

            if (isRegistering) {

                await registerUser(email, password);

            } else {

                await loginUser(email, password);

            }

            setPassword("");

        } catch (err) {

            setAuthError(err.message);

        }

    }

    // -------------------------------
    // LOGOUT
    // -------------------------------

    async function handleLogout() {

        try {

            await logoutUser();

        } catch (err) {

            setAuthError(err.message);

        }

    }

    // -------------------------------
    // RETRIEVE MESSAGES
    // -------------------------------

    useEffect(() => {
        let cancelled = false;

        if (!user || authLoading) {
            setMessages([]);
            setError("");
            return;
        }

        async function loadMessages() {
            try {
                const token = await getUserToken(user);

                const data = await getMessages(token);

                if (!cancelled) {
                    setMessages(data);
                    setError("");
                }

            } catch (err) {
                if (!cancelled) {
                    setError(err.message);
                }
            }
        }

        loadMessages();

        return () => {
            cancelled = true;
        };

    }, [user, authLoading]);

    async function loadMessages() {
        if (!user) return;

        try {
            const token = await getUserToken(user);

            const data = await getMessages(token);

            setMessages(data);
            setError("");

        } catch (err) {
            setError(err.message);
        }
    }



    // -------------------------------
    // CREATE MESSAGE
    // -------------------------------

    async function handleSubmit(event) {
        event.preventDefault();

        if (!content.trim() || !user) return;

        setLoading(true);
        setError("");

        try {
            const token = await getUserToken(user);

            await createMessage(content, token);

            setContent("");

            await loadMessages();

        } catch (err) {
            setError(err.message);

        } finally {
            setLoading(false);
        }
    }


    // -------------------------------
    // APPLICATION INTERFACE
    // -------------------------------

    if (authLoading) {

        return <div className="app">Loading authentication...</div>;

    }

    return (

        <div className="app">

            <h1>Jomini Library</h1>

            <p>Logistics Training and Evaluation Platform</p>

            <hr />

            <h2>Firebase Authentication</h2>

            {!user ? (

                <div>

                    <h3>
                        {isRegistering ? "Create Account" : "Login"}
                    </h3>

                    <form onSubmit={handleAuthSubmit}>

                        <input
                            type="email"
                            value={email}
                            onChange={(event) => setEmail(event.target.value)}
                            placeholder="Email address"
                            required
                        />

                        <input
                            type="password"
                            value={password}
                            onChange={(event) => setPassword(event.target.value)}
                            placeholder="Password"
                            required
                        />

                        <button type="submit">
                            {isRegistering ? "Register" : "Login"}
                        </button>

                    </form>

                    {authError && (
                        <p className="error">{authError}</p>
                    )}

                    <button
                        onClick={() => {
                            setIsRegistering(!isRegistering);
                            setAuthError("");
                        }}
                    >
                        {isRegistering
                            ? "Already have an account? Login"
                            : "Need an account? Register"}
                    </button>

                </div>

            ) : (

                <div>

                    <h3>Welcome!</h3>

                    <p>
                        Logged in as: {user.email}
                    </p>

                   <p>
                    Firebase UID: {user.uid}
                    </p>

                    <hr />

                    <h3>PostgreSQL User Profile</h3>

                    {profileLoading && (
                        <p>Loading PostgreSQL profile...</p>
                    )}

                    {profileError && (
                        <p className="error">
                            PostgreSQL Error: {profileError}
                        </p>
                    )}

                    {profile && (
                        <div>
                            <p>
                                <strong>Database User ID:</strong> {profile.id}
                            </p>

                            <p>
                                <strong>Email:</strong> {profile.email}
                            </p>

                            <p>
                                <strong>Display Name:</strong> {profile.display_name || "Not provided"}
                            </p>

                            <p>
                                <strong>Firebase UID:</strong> {profile.firebase_uid}
                            </p>

                            <p>
                                <strong>Account Created:</strong> {new Date(profile.created_at).toLocaleString()}
                            </p>
                        </div>
                    )}

                    <button onClick={handleLogout}>
                        Logout
                    </button>


                    {authError && (
                        <p className="error">{authError}</p>
                    )}

                </div>

            )}

            <hr />

            <h2>Message Database Test</h2>

            <form onSubmit={handleSubmit}>

                <input
                    type="text"
                    value={content}
                    onChange={(event) => setContent(event.target.value)}
                    placeholder="Enter a message..."
                />

                <button type="submit" disabled={loading}>
                    {loading ? "Sending..." : "Send Message"}
                </button>

            </form>

            {error && <p className="error">{error}</p>}

            <h3>Saved Messages</h3>

            <button onClick={loadMessages}>
                Refresh Messages
            </button>

            <ul>

                {messages.map((message) => (

                    <li key={message.id}>
                        {message.content}
                    </li>

                ))}

            </ul>

        </div>

    );

}

export default App;

