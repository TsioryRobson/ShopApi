"""
Modèles Pydantic pour les Produits.

Pydantic valide automatiquement les données entrantes.
- ProductBase    → champs communs (nom, catégorie, prix)
- ProductCreate  → ce que le client envoie pour CRÉER un produit
- ProductUpdate  → ce que le client envoie pour MODIFIER (tout est optionnel)
- ProductOut     → ce que l'API RENVOIE au client (avec l'id)
"""

from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    """Champs communs à toutes les opérations sur un produit."""

    name: str = Field(..., min_length=1, max_length=255, description="Nom du produit")

    category_id: int = Field(..., description="Identifiant de la catégorie du produit")

    price: float = Field(..., gt=0, description="Prix du produit")


class ProductCreate(ProductBase):
    """
    Schéma pour CRÉER un produit.
    Hérite de ProductBase → tous les champs sont obligatoires.
    """

    pass


class ProductUpdate(BaseModel):
    """
    Schéma pour MODIFIER un produit.
    Tous les champs sont optionnels → mise à jour partielle possible.
    """

    name: Optional[str] = Field(
        default=None, min_length=1, max_length=255, description="Nouveau nom du produit"
    )

    category_id: Optional[int] = Field(
        default=None, description="Nouvelle catégorie du produit"
    )

    price: Optional[float] = Field(
        default=None, gt=0, description="Nouveau prix du produit"
    )


class ProductOut(ProductBase):
    """
    Schéma de SORTIE → ce que l'API renvoie au client.
    Inclut l'id généré automatiquement.
    category_id est optionnel pour les cas où la catégorie a été supprimée.
    """

    id: int = Field(..., description="Identifiant unique du produit")
    category_id: Optional[int] = Field(default=None, description="Identifiant de la catégorie")

    model_config = {"from_attributes": True}
