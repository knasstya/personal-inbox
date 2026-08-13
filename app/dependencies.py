from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.auth import decode_access_token
from app.db.database import SessionLocal
from app.models import User

security = HTTPBearer()


def get_current_username(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user
    finally:
        db.close()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        return user.id
    finally:
        db.close()