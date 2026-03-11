"""
Utilitaires de sécurité — hashage et vérification des mots de passe.

Utilise hashlib (stdlib Python) avec SHA-256 + salt aléatoire.
Format stocké en base : "<salt>:<hash>"

Note : en production, préférer passlib[bcrypt] pour une résistance
aux attaques par force brute (bcrypt est intentionnellement lent).
Installation : poetry add "passlib[bcrypt]"
"""

import hashlib
import secrets
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """
    Hache un mot de passe avec un salt aléatoire.

    Args:
        plain_password: Le mot de passe en clair.

    Returns:
        str: La chaîne "<salt>:<hash>" à stocker en base.
    """
    # Optionnel : conserver le hash legacy (salt:sha256) ou utiliser passlib to_hash
    # Ici on laisse la méthode existante (legacy) pour compatibilité
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Supporte deux formats :
      - legacy: "<salt>:<sha256hex>"
      - passlib/bcrypt standard (ex: "$2b$...") -> vérifié via passlib
    Retourne True si correspond, False sinon.
    """
    if not hashed_password:
        return False
    # legacy format detect (contains a single colon)
    try:
        if ":" in hashed_password:
            salt, stored_hash = hashed_password.split(":", 1)
            computed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
            return secrets.compare_digest(computed, stored_hash)
        # else try passlib (bcrypt etc.)
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crée un token d'accès.

    Args:
        data: Les données à encoder.
        expires_delta: Durée d'expiration (optionnel).

    Returns:
        str: Le token d'accès.
    """
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
