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


def hash_password(plain_password: str) -> str:
    """
    Hache un mot de passe avec un salt aléatoire.

    Args:
        plain_password: Le mot de passe en clair.

    Returns:
        str: La chaîne "<salt>:<hash>" à stocker en base.
    """
    salt = secrets.token_hex(16)  # 32 caractères hex aléatoires
    hashed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe en clair correspond au hash stocké.

    Args:
        plain_password: Le mot de passe soumis par l'utilisateur.
        hashed_password: Le hash stocké en base (format "salt:hash").

    Returns:
        bool: True si le mot de passe est correct, False sinon.
    """
    try:
        salt, stored_hash = hashed_password.split(":")
        computed = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return secrets.compare_digest(computed, stored_hash)
    except (ValueError, AttributeError):
        return False
