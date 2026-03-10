"""
Router pour les Catégories — les 4 endpoints CRUD.

Chaque endpoint :
1. Reçoit la requête HTTP (FastAPI gère la validation grâce à Pydantic)
2. Appelle le service (logique métier)
3. Retourne la réponse

Les tags et descriptions enrichissent la documentation Swagger automatique.
"""

from fastapi import APIRouter, status
from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut
from app.services import category_service

# Création du router avec un préfixe et un tag pour Swagger
router = APIRouter(
    prefix="/categories",
    tags=["Catégories"],
    responses={404: {"description": "Catégorie introuvable"}},
)


@router.get(
    "/",
    response_model=list[CategoryOut],
    summary="Lister toutes les catégories",
    description="Retourne la liste complète des catégories disponibles.",
)
def list_categories():
    """GET /categories → liste toutes les catégories."""
    return category_service.get_all_categories()


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    summary="Obtenir une catégorie par son ID",
    description="Retourne une catégorie spécifique. Erreur 404 si l'ID n'existe pas.",
)
def get_category(category_id: int):
    """GET /categories/{id} → détails d'une catégorie."""
    return category_service.get_category(category_id)


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une nouvelle catégorie",
    description="Crée une catégorie avec un nom (obligatoire) et une description (optionnelle).",
)
def create_category(category: CategoryCreate):
    """POST /categories → crée une catégorie."""
    return category_service.create_category(category)


@router.put(
    "/{category_id}",
    response_model=CategoryOut,
    summary="Modifier une catégorie",
    description="Met à jour les champs envoyés d'une catégorie existante. Erreur 404 si l'ID n'existe pas.",
)
def update_category(category_id: int, category: CategoryUpdate):
    """PUT /categories/{id} → modifie une catégorie."""
    return category_service.update_category(category_id, category)


@router.delete(
    "/{category_id}",
    summary="Supprimer une catégorie",
    description="Supprime une catégorie par son ID. Erreur 404 si l'ID n'existe pas.",
)
def delete_category(category_id: int):
    """DELETE /categories/{id} → supprime une catégorie."""
    return category_service.delete_category(category_id)
