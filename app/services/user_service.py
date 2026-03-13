"""
Service pour les Utilisateurs — logique métier.

Gère :
- Les erreurs 404 (utilisateur introuvable)
- Les conflits 409 (username ou email déjà pris)
- Le hashage du mot de passe avant stockage
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import UserCreate, UserUpdate, UserOut
from app.repositories import user_repo
from app.core.passwords import hash_password, verify_password


def get_all_users(db: Session) -> list[UserOut]:
    """Récupère tous les utilisateurs."""
    users = user_repo.get_all(db)
    return [UserOut.model_validate(u) for u in users]


def get_user(db: Session, user_id: int) -> UserOut:
    """Récupère un utilisateur par son id. Lève 404 si introuvable."""
    user = user_repo.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'id {user_id} introuvable",
        )
    return UserOut.model_validate(user)


def get_user_by_username(db: Session, username: str):
    """Récupère un utilisateur par son username (retourne UserOut ou None)."""
    user = user_repo.get_by_username(db, username)
    return UserOut.model_validate(user) if user else None


def get_user_by_email(db: Session, email: str):
    """Récupère un utilisateur par son email (retourne UserOut ou None)."""
    user = user_repo.get_by_email(db, email)
    return UserOut.model_validate(user) if user else None


def create_user(db: Session, data: UserCreate | dict) -> UserOut:
    """
    Crée un nouvel utilisateur.
    Accepte soit un UserCreate, soit un dictionnaire {username, email, password}.
    Lève 409 si le username ou l'email est déjà utilisé.
    """
    # Normalize input
    if isinstance(data, dict):
        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
    else:
        username = data.username
        email = data.email
        password = data.password

    # Check for conflicts
    if user_repo.get_by_username(db, username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Le username '{username}' est déjà utilisé",
        )
    if user_repo.get_by_email(db, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"L'email '{email}' est déjà utilisé",
        )

    # Hash password and create user
    hashed = hash_password(password)
    user = user_repo.create(db, username, email, hashed)
    return UserOut.model_validate(user)


def update_user(db: Session, user_id: int, data: UserUpdate) -> UserOut:
    """
    Met à jour un utilisateur existant.
    Lève 404 si introuvable, 409 si le nouveau username/email est déjà pris.
    """
    # Vérifie que l'utilisateur existe
    existing = user_repo.get_by_id(db, user_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'id {user_id} introuvable",
        )

    # Vérifie les conflits uniquement si les champs changent
    if data.username is not None and data.username != existing.username:
        if user_repo.get_by_username(db, data.username) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Le username '{data.username}' est déjà utilisé",
            )

    if data.email is not None and data.email != existing.email:
        if user_repo.get_by_email(db, data.email) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"L'email '{data.email}' est déjà utilisé",
            )

    # Prépare les données à mettre à jour
    update_data = data.model_dump(exclude_unset=True)

    # Si un nouveau mot de passe est fourni, on le hache
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    updated = user_repo.update(db, user_id, update_data)
    return UserOut.model_validate(updated)


def delete_user(db: Session, user_id: int) -> dict:
    """Supprime un utilisateur. Lève 404 si introuvable."""
    deleted = user_repo.delete(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Utilisateur avec l'id {user_id} introuvable",
        )
    return {"message": f"Utilisateur {user_id} supprimé avec succès"}


def get_user_by_email(db: Session, email: str):
    """Récupère un utilisateur par son email. Retourne None si introuvable."""
    return user_repo.get_by_email(db, email)


def authenticate_user(db: Session, email: str, password: str):
    """
    Vérifie les identifiants et retourne l'objet user DB si valides.

    Retourne None si l'utilisateur n'existe pas ou si le mot de passe est incorrect.
    """
    user = user_repo.get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user