// Purpose: Connect frontend app to firebase and setup firebase authentication

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Firebase configuration from .env.local
// Got from https://github.com/firebase/quickstart-js/blob/474e779bc3f0af1c620fb9dfa53e933e6aa3edd7/auth/config.ts#L1-L12
// you have to add VITE_ for vite to see it
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);

export default app;
//debugging
console.log("Firebase configuration check:", {
  apiKey: Boolean(import.meta.env.VITE_FIREBASE_API_KEY),
  authDomain: Boolean(import.meta.env.VITE_FIREBASE_AUTH_DOMAIN),
  projectId: Boolean(import.meta.env.VITE_FIREBASE_PROJECT_ID),
  appId: Boolean(import.meta.env.VITE_FIREBASE_APP_ID),
});
