"""
Schémas Pydantic pour les Utilisateurs.

- UserBase    → champs communs (username, email)
- UserCreate  → ce que le client envoie pour créer un compte (+ password)
- UserUpdate  → mise à jour partielle (tous les champs optionnels)
- UserOut     → ce que l'API renvoie (jamais le mot de passe)
"""

from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    """Champs communs à toutes les opérations sur un utilisateur."""

    username: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Nom d'utilisateur unique",
        examples=["johndoe"],
    )
    email: str = Field(
        ...,
        max_length=100,
        description="Adresse email unique",
        examples=["john@example.com"],
    )


class UserCreate(UserBase):
    """
    Schéma pour CRÉER un utilisateur.
    Hérite de UserBase + champ password obligatoire.
    """

    password: str = Field(
        ..., min_length=6, description="Mot de passe (minimum 6 caractères)"
    )


class UserUpdate(BaseModel):
    """
    Schéma pour MODIFIER un utilisateur.
    Tous les champs sont optionnels → mise à jour partielle.
    """

    username: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Nouveau nom d'utilisateur",
    )
    email: Optional[str] = Field(
        default=None, max_length=100, description="Nouvelle adresse email"
    )
    password: Optional[str] = Field(
        default=None, min_length=6, description="Nouveau mot de passe"
    )


class UserOut(BaseModel):
    """
    Schéma de SORTIE → ce que l'API renvoie.
    Le mot de passe haché n'est JAMAIS exposé.
    """

    id: int = Field(..., description="Identifiant unique de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur")
    email: str = Field(..., description="Adresse email")

    model_config = {"from_attributes": True}

class Login(BaseModel):
    """Payload attendu pour la connexion."""
    email: str = Field(..., description="Email de l'utilisateur")
    password: str = Field(..., description="Mot de passe en clair")


class Token(BaseModel):
    """Réponse retournée après authentification."""
    access_token: str = Field(..., description="JWT d'accès")
    token_type: str = Field(..., description="Type de token, ex: 'bearer'")


class TokenData(BaseModel):
    """Données extraites du token (ex: sub/email)."""
    email: Optional[str] = None