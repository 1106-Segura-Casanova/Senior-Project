# Purpose: Handle communication between the backend and firebase authentication.

import os
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import auth

# Load environment variables
load_dotenv()

# Retrieve Firebase project ID
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
if not FIREBASE_PROJECT_ID:
    raise RuntimeError(
        "FIREBASE_PROJECT_ID is missing from the backend .env file."
    )

# Initialize Firebase Admin using Google Application Default Credentials
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    firebase_app = firebase_admin.initialize_app(
        options={
            "projectId": FIREBASE_PROJECT_ID
        }
    )

def verify_firebase_token(id_token: str) -> dict:
    """
    Verify a Firebase ID token and return its decoded claims.
    """
    decoded_token = auth.verify_id_token(
        id_token,
        app=firebase_app
    )
    return decoded_token
