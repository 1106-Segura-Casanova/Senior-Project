// Purpose: Handle user authentication in firebase

import { auth } from "../config/firebase";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "firebase/auth";

// Register a new user
export async function registerUser(email, password) {
    const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
    );

    return userCredential.user;
}

// Log in an existing user
export async function loginUser(email, password) {
    const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
    );

    return userCredential.user;
}

// Log out the current user
export async function logoutUser() {
    await signOut(auth);
}

// Monitor whether a user is logged in or logged out
export function subscribeToAuthChanges(callback) {
    return onAuthStateChanged(auth, callback);
}

// Retrieve a Firebase ID token for backend authentication
export async function getUserToken(user) {
    if (!user) {
        throw new Error("No authenticated user found.");
    }

    return await user.getIdToken();
}
