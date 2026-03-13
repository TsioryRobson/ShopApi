"""
Routeur d’authentification compatible avec security.py
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from pydantic import BaseModel, Field

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.services.user_service import authenticate_user, get_user_by_email, create_user
from app.models.user import Login, Token, UserOut
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# REGISTER
# -------------------------

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=1)
    email: str
    password: str = Field(..., min_length=6)


@router.post("/register", response_model=Token, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):

    if get_user_by_email(db, payload.email):
        raise HTTPException(409, f"L'email '{payload.email}' est déjà utilisé.")

    # création utilisateur
    user = create_user(db, {
        "username": payload.username,
        "email": payload.email,
        "password": payload.password,
    })

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}


# -------------------------
# LOGIN
# -------------------------

@router.post("/login", response_model=Token)
def login(payload: Login, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            401, "Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


# -------------------------
# ME (utilise security.py)
# -------------------------

@router.get("/me", response_model=UserOut)
def me(current_user: UserOut = Depends(get_current_user)):
    return current_user


# -------------------------
# LOGOUT
# -------------------------

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully (client-side)"}