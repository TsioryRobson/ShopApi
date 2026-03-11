"""
Repository pour les Categories — acces a la base de donnees Postgres.

Utilise SQLAlchemy pour toutes les operations CRUD.
Chaque fonction recoit une session DB (injectee par FastAPI via Depends).
"""

from sqlalchemy.orm import Session
from app.models.tables import CategoryDB
from app.models.category import CategoryCreate, CategoryUpdate


def get_all(db: Session) -> list[CategoryDB]:
    """Retourne toutes les categories depuis la DB."""
    return db.query(CategoryDB).all()


def get_by_id(db: Session, category_id: int) -> CategoryDB | None:
    """Retourne une categorie par son id, ou None si introuvable."""
    return db.query(CategoryDB).filter(CategoryDB.id == category_id).first()


def create(db: Session, data: CategoryCreate) -> CategoryDB:
    """Cree une nouvelle categorie dans la DB."""
    new_category = CategoryDB(
        name=data.name,
        description=data.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def update(db: Session, category_id: int, data: CategoryUpdate) -> CategoryDB | None:
    """Met a jour une categorie existante. Retourne None si introuvable."""
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if category is None:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


def delete(db: Session, category_id: int) -> bool:
    """Supprime une categorie. Retourne True si supprimee, False sinon."""
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if category is None:
        return False

    db.delete(category)
    db.commit()
    return True
