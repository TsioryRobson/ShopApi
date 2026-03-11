"""
Repository pour les Utilisateurs — accès à la base de données.

Suivant le même style que category_repo (fonctions, pas de classe).
Chaque fonction reçoit une session DB injectée par FastAPI via Depends.
"""

from sqlalchemy.orm import Session
from app.models.tables import UserDB


def get_all(db: Session) -> list[UserDB]:
    """Retourne tous les utilisateurs depuis la DB."""
    return db.query(UserDB).all()


def get_by_id(db: Session, user_id: int) -> UserDB | None:
    """Retourne un utilisateur par son id, ou None si introuvable."""
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def get_by_username(db: Session, username: str) -> UserDB | None:
    """Retourne un utilisateur par son username, ou None si introuvable."""
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_by_email(db: Session, email: str) -> UserDB | None:
    """Retourne un utilisateur par son email, ou None si introuvable."""
    return db.query(UserDB).filter(UserDB.email == email).first()


def create(db: Session, username: str, email: str, hashed_password: str) -> UserDB:
    """Crée un nouvel utilisateur dans la DB."""
    new_user = UserDB(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update(db: Session, user_id: int, update_data: dict) -> UserDB | None:
    """
    Met à jour un utilisateur existant.
    Retourne None si l'utilisateur est introuvable.
    update_data ne doit contenir que les champs à modifier.
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        return None

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user_id: int) -> bool:
    """Supprime un utilisateur. Retourne True si supprimé, False sinon."""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        return False

    db.delete(user)
    db.commit()
    return True
