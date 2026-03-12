"""
Service pour les Categories — logique metier.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.repositories import category_repo


def get_all_categories(db: Session) -> list[CategoryOut]:
    """Recupere toutes les categories."""
    categories = category_repo.get_all(db)
    return [CategoryOut.model_validate(cat, from_attributes=True) for cat in categories]


def get_category(db: Session, category_id: int) -> CategoryOut:
    """Recupere une categorie par son id. Leve 404 si introuvable."""
    category = category_repo.get_by_id(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categorie avec l'id {category_id} introuvable",
        )
    return CategoryOut.model_validate(category, from_attributes=True)


def create_category(db: Session, data: CategoryCreate) -> CategoryOut:
    """Cree une nouvelle categorie."""
    category = category_repo.create(db, data)
    return CategoryOut.model_validate(category, from_attributes=True)


def update_category(db: Session, category_id: int, data: CategoryUpdate) -> CategoryOut:
    """Met a jour une categorie existante. Leve 404 si introuvable."""
    updated = category_repo.update(db, category_id, data)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categorie avec l'id {category_id} introuvable",
        )
    return CategoryOut.model_validate(updated, from_attributes=True)


def delete_category(db: Session, category_id: int) -> dict:
    """Supprime une categorie. Leve 404 si introuvable."""
    deleted = category_repo.delete(db, category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categorie avec l'id {category_id} introuvable",
        )
    return {"message": f"Categorie {category_id} supprimee avec succes"}
