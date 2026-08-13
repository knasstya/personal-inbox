from sqlalchemy.exc import IntegrityError

from app.db.database import SessionLocal
from app.models import User
from app.services.security import hash_password, verify_password


def create_user(username: str, email: str, password: str):
    db = SessionLocal()

    try:
        hashed_password = hash_password(password)

        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise

    finally:
        db.close()

def authenticate_user(username: str, password: str):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    finally:
        db.close()