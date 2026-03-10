"""
Service pour les Catégories — couche de logique métier.

Architecture en couches (Clean Architecture simplifiée) :
  Router → Service → Repository
  
Le service :
- Reçoit les données validées du router
- Applique la logique métier (vérifications, règles)
- Appelle le repository pour l'accès aux données
- Lève des exceptions HTTP si quelque chose ne va pas
"""

from fastapi import HTTPException, status
from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.repositories import category_repo


def get_all_categories() -> list[CategoryOut]:
    """Récupère toutes les catégories."""
    return category_repo.get_all()


def get_category(category_id: int) -> CategoryOut:
    """
    Récupère une catégorie par son id.
    Lève 404 si introuvable.
    """
    category = category_repo.get_by_id(category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catégorie avec l'id {category_id} introuvable"
        )
    return category


def create_category(data: CategoryCreate) -> CategoryOut:
    """Crée une nouvelle catégorie."""
    return category_repo.create(data)


def update_category(category_id: int, data: CategoryUpdate) -> CategoryOut:
    """
    Met à jour une catégorie existante.
    Lève 404 si introuvable.
    """
    updated = category_repo.update(category_id, data)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catégorie avec l'id {category_id} introuvable"
        )
    return updated


def delete_category(category_id: int) -> dict:
    """
    Supprime une catégorie.
    Lève 404 si introuvable.
    Retourne un message de confirmation.
    """
    deleted = category_repo.delete(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Catégorie avec l'id {category_id} introuvable"
        )
    return {"message": f"Catégorie {category_id} supprimée avec succès"}
