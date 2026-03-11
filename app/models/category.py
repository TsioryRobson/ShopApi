"""
Modèles Pydantic pour les Catégories.

Pydantic valide automatiquement les données entrantes.
- CategoryBase    → champs communs (nom, description)
- CategoryCreate  → ce que le client envoie pour CRÉER une catégorie
- CategoryUpdate  → ce que le client envoie pour MODIFIER (tout est optionnel)
- CategoryOut     → ce que l'API RENVOIE au client (avec l'id)
"""

from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    """Champs communs à toutes les opérations sur une catégorie."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nom de la catégorie",
        examples=["Électronique"],
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Description optionnelle de la catégorie",
        examples=["Appareils et gadgets électroniques"],
    )


class CategoryCreate(CategoryBase):
    """
    Schéma pour CRÉER une catégorie.
    Hérite de CategoryBase → name obligatoire, description optionnelle.
    """

    pass


class CategoryUpdate(BaseModel):
    """
    Schéma pour MODIFIER une catégorie.
    Tous les champs sont optionnels → on ne met à jour que ce qui est envoyé.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Nouveau nom de la catégorie",
    )
    description: Optional[str] = Field(
        default=None, max_length=500, description="Nouvelle description de la catégorie"
    )


class CategoryOut(CategoryBase):
    """
    Schéma de SORTIE → ce que l'API renvoie au client.
    Inclut l'id généré automatiquement.
    """

    id: int = Field(..., description="Identifiant unique de la catégorie")
