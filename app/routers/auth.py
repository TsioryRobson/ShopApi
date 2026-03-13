"""
Router pour l'Authentification — login, register, logout.

Utilise JWT token stocké en localStorage côté client.
Format token : JWT signé avec SECRET_KEY depuis config.
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from jose import JWTError, jwt

from app.core.database import get_db
from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.models.user import UserOut
from app.services import user_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={401: {"description": "Unauthorized"}, 409: {"description": "Conflict"}},
)


# Schémas Pydantic
class LoginRequest(BaseModel):
    """Schéma pour la connexion."""
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)


class RegisterRequest(BaseModel):
    """Schéma pour l'inscription."""
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Schéma pour la réponse de token."""
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class AuthUser(BaseModel):
    """Utilisateur extrait du token JWT."""
    user_id: int
    username: str


def create_access_token(user_id: int, username: str) -> str:
    """
    Crée un JWT token.

    Args:
        user_id: ID de l'utilisateur.
        username: Username de l'utilisateur.

    Returns:
        str: Token JWT signé.
    """
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def verify_token(token: str) -> AuthUser:
    """
    Vérifie et décode un JWT token.

    Args:
        token: JWT token à vérifier.

    Returns:
        AuthUser: Les données utilisateur du token.

    Raises:
        JWTError: Si le token est invalide ou expiré.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        username: str = payload.get("username")

        if user_id is None or username is None:
            raise JWTError("Invalid token payload")

        return AuthUser(user_id=user_id, username=username)
    except (JWTError, ValueError, TypeError):
        raise JWTError("Invalid or expired token")


def get_current_user(
    authorization: str | None = None,
    db: Session = Depends(get_db),
) -> UserOut:
    """
    Dépendance FastAPI pour extraire l'utilisateur courant du token.

    Args:
        authorization: Header "Authorization: Bearer <token>".
        db: Session DB.

    Returns:
        UserOut: L'utilisateur courant.

    Raises:
        HTTPException: Si le token est absent ou invalide.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # Enlever "Bearer "

    try:
        auth_user = verify_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_service.get_user(db, auth_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, summary="Register a new user")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user and return a JWT token.

    Args:
        request: Registration data (username, email, password).
        db: SQLAlchemy database session.

    Returns:
        TokenResponse: JWT token and user info.

    Raises:
        HTTPException 409: If username or email is already taken.
    """
    # Check if user already exists
    existing = user_service.get_user_by_username(db, request.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{request.username}' already exists",
        )

    existing_email = user_service.get_user_by_email(db, request.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{request.email}' already in use",
        )

    # Create user (password is hashed by the service)
    new_user = user_service.create_user(
        db,
        user_data_dict={
            "username": request.username.strip(),
            "email": request.email.strip(),
            "password": request.password,
        },
    )

    # Generate token
    token = create_access_token(new_user.id, new_user.username)

    return TokenResponse(access_token=token, user=new_user)


@router.post("/login", response_model=TokenResponse, summary="Login with username and password")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and return a JWT token.

    Args:
        request: Login data (username, password).
        db: SQLAlchemy database session.

    Returns:
        TokenResponse: JWT token and user info.

    Raises:
        HTTPException 401: If credentials are invalid.
    """
    # Get user by username
    user = user_service.get_user_by_username(db, request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate token
    token = create_access_token(user.id, user.username)

    return TokenResponse(access_token=token, user=user)


@router.post("/me", response_model=UserOut, summary="Get current authenticated user")
def get_me(authorization: str | None = None, db: Session = Depends(get_db)):
    """
    Return the currently authenticated user from the token.

    Args:
        authorization: Header "Authorization: Bearer <token>".
        db: SQLAlchemy database session.

    Returns:
        UserOut: The current user.

    Raises:
        HTTPException 401: If not authenticated.
    """
    return get_current_user(authorization, db)


@router.post("/logout", summary="Logout (client-side token invalidation)")
def logout():
    """
    Logout endpoint (token invalidation happens client-side).

    Returns:
        dict: Success message.
    """
    return {"message": "Logged out successfully"}
