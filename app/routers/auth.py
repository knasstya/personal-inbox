from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.schemas.users import UserCreate, UserLogin, UserResponse, Token
from app.services.users import (
    authenticate_user,
    create_user as create_user_service,
)
from app.services.auth import create_access_token


router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    try:
        return create_user_service(
            user.username,
            user.email,
            user.password,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists",
        )

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    authenticated_user = authenticate_user(
        user.username,
        user.password,
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token(authenticated_user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }