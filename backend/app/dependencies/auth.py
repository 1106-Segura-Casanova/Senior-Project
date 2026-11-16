# Purpose: Make sure users are logged in and identify who they are

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from firebase_admin.exceptions import FirebaseError
from app.database.connection import get_db
from app.models.user import User
from app.services.firebase_service import verify_firebase_token

security = HTTPBearer()
# Recieved from FastAPI github at https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/security/tutorial004.py#L89-L106
# Debugged with help from Chat gpt
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Verify the Firebase ID token and retrieve the
    corresponding PostgreSQL user.
    """
    id_token = credentials.credentials
    try:
        decoded_token = verify_firebase_token(id_token)
    except FirebaseError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token",
        )
    firebase_uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    display_name = decoded_token.get("name")
    if not firebase_uid or not email:
        raise HTTPException(
            status_code=401,
            detail="Firebase token is missing required user information",
        )
    user = (
        db.query(User)
        .filter(User.firebase_uid == firebase_uid)
        .first()
    )
    #Taken from FastAPi github https://github.com/fastapi/fastapi/blob/0.110.0/docs_src/sql_databases/sql_app/crud.py#L20-L21
    if user is None:
        user = User(
            firebase_uid=firebase_uid,
            email=email,
            display_name=display_name,
        )
        db.add(user)
    else:
        user.email = email
        if display_name:
            user.display_name = display_name
    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise
    return user
