// Purpose: Handle user authentication in firebase

import { auth } from "../config/firebase";
import {
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "firebase/auth";

// Register a new user
// Got from Firebase https://github.com/firebase/snippets-web/blob/fbccd85f8f796d18ccf4b6b844298ccdfb4b772f/snippets/auth-next/email/auth_signup_password.js#L8-L14
export async function registerUser(email, password) {
    const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
    );

    return userCredential.user;
}

// Log in an existing user
// Got from Firebase https://github.com/firebase/snippets-web/blob/fbccd85f8f796d18ccf4b6b844298ccdfb4b772f/snippets/auth-next/email/auth_signin_password.js#L8-L14
export async function loginUser(email, password) {
    const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
    );

    return userCredential.user;
}

// Log out the current user
// Got from Firebase https://github.com/firebase/snippets-web/blob/fbccd85f8f796d18ccf4b6b844298ccdfb4b772f/snippets/auth-next/index/auth_sign_out.js#L8-L11
export async function logoutUser() {
    await signOut(auth);
}

// Got from Chat 
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
