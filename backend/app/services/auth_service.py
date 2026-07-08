from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user_model import User
from app.schemas.auth_schema import RegisterRequest

from app.schemas.auth_schema import LoginRequest
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(db: Session, request: RegisterRequest):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        return None

    hashed_password = pwd_context.hash(request.password)

    user = User(
        name=request.name,
        email=request.email,
        password=hashed_password,
        role="admin"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def login_user(db: Session, request: LoginRequest):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        return None

    if not pwd_context.verify(request.password, user.password):
        return None

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return token