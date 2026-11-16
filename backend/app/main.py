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
#Implemented from FastAPI https://github.com/fastapi/fastapi/blob/e1144f6954eb8dd8c306f8dd2f5f0a14bbeb2cfd/docs_src/cors/tutorial001.py#L13-L19
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

#Implemented from FastAPI https://github.com/fastapi/fastapi/blob/e1144f6954eb8dd8c306f8dd2f5f0a14bbeb2cfd/docs_src/cors/tutorial001.py#L22-L24
@app.get("/")
def home():
    return {
        "message": "Jomini Library API is running!"
    }