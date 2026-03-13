"""
Router pour les Categories — les 4 endpoints CRUD.
Utilise Depends(get_db) pour injecter une session DB dans chaque endpoint.
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.services import category_service
from app.core.security import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Categorie introuvable"}},
)


@router.get(
    "/", response_model=list[CategoryOut], summary="Lister toutes les categories"
)
def list_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db)


@router.get(
    "/{category_id}", response_model=CategoryOut, summary="Obtenir une categorie par ID"
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db, category_id)


@router.post(
    "/", 
    response_model=CategoryOut, 
    status_code=status.HTTP_201_CREATED, 
    summary="Creer une categorie",
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return category_service.create_category(db, category)


@router.put(
    "/{category_id}", response_model=CategoryOut, summary="Modifier une categorie"
)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return category_service.update_category(db, category_id, category)


@router.delete("/{category_id}", summary="Supprimer une categorie")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.delete_category(db, category_id)
