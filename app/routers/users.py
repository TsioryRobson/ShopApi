"""
Router pour les Utilisateurs — les 5 endpoints CRUD.

Endpoints :
  GET    /users/          → lister tous les utilisateurs
  GET    /users/{id}      → obtenir un utilisateur par ID
  POST   /users/          → créer un utilisateur
  PUT    /users/{id}      → modifier un utilisateur (partiel)
  DELETE /users/{id}      → supprimer un utilisateur
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserCreate, UserUpdate, UserOut
from app.services import user_service
from app.core.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Utilisateur introuvable"}},
    dependencies=[Depends(get_current_user)]  # Protéger tous les endpoints par auth
)


@router.get("/", response_model=list[UserOut], summary="Lister tous les utilisateurs")
def list_users(db: Session = Depends(get_db)):
    """Retourne la liste de tous les utilisateurs enregistrés."""
    return user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserOut, summary="Obtenir un utilisateur par ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retourne un utilisateur par son identifiant. 404 si introuvable."""
    return user_service.get_user(db, user_id)


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un utilisateur"
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.
    - **409** si le username ou l'email est déjà utilisé.
    - Le mot de passe est haché avant stockage (jamais exposé en réponse).
    """
    return user_service.create_user(db, user)


@router.put("/{user_id}", response_model=UserOut, summary="Modifier un utilisateur")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un utilisateur existant (mise à jour partielle possible).
    - **404** si l'utilisateur est introuvable.
    - **409** si le nouveau username ou email est déjà pris.
    """
    return user_service.update_user(db, user_id, user)


@router.delete(
    "/{user_id}",
    summary="Supprimer un utilisateur",
    responses={200: {"description": "Utilisateur supprimé avec succès"}}
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprime définitivement un utilisateur.
    - **404** si l'utilisateur est introuvable.
    """
    return user_service.delete_user(db, user_id)
