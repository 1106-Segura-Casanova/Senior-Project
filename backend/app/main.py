# Purpose: Creates the FastAPI app

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.message_controller import router
from app.controllers.auth_controller import auth_router

# Create application
app = FastAPI(
    title="Jomini Library API",
    version="0.1.0"
)

# Allow React frontend to communicate with Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register controller routes
app.include_router(router)
app.include_router(auth_router)
@app.get("/")
def home():
    return {
        "message": "Jomini Library API is running!"
    }