# Purpose: Allows the frontend to send the backend a request for information about the currently logged-in user.

from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.models.user import User

#Implemented or trimmed from FastAPI docs https://fastapi.tiangolo.com/tutorial/bigger-applications/#import-the-dependencies
auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)

# Implemented from FastAPI docs https://fastapi.tiangolo.com/tutorial/security/get-current-user/#get-the-user
@auth_router.get("/me")
def get_current_user_profile(
    user: User = Depends(get_current_user),
):
    return {
        "id": user.id,
        "firebase_uid": user.firebase_uid,
        "email": user.email,
        "display_name": user.display_name,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
 