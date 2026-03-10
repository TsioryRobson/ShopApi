"""
Repository pour les Catégories — couche d'accès aux données.

Pattern Repository : sépare la LOGIQUE MÉTIER du STOCKAGE.
→ Aujourd'hui : liste en mémoire (KISS, simple, ça marche)
→ Demain : on remplace par SQLAlchemy + PostgreSQL sans toucher aux routes.

Principe XP : on ne code que ce dont on a besoin MAINTENANT.
"""

from app.models.category import CategoryCreate, CategoryUpdate, CategoryOut


# Stockage en mémoire — simple et fonctionnel
_categories: list[dict] = []
_next_id: int = 1


def get_all() -> list[CategoryOut]:
    """Retourne toutes les catégories."""
    return [CategoryOut(**cat) for cat in _categories]


def get_by_id(category_id: int) -> CategoryOut | None:
    """Retourne une catégorie par son id, ou None si introuvable."""
    for cat in _categories:
        if cat["id"] == category_id:
            return CategoryOut(**cat)
    return None


def create(data: CategoryCreate) -> CategoryOut:
    """Crée une nouvelle catégorie et retourne la catégorie créée."""
    global _next_id

    new_category = {
        "id": _next_id,
        "name": data.name,
        "description": data.description,
    }
    _categories.append(new_category)
    _next_id += 1

    return CategoryOut(**new_category)


def update(category_id: int, data: CategoryUpdate) -> CategoryOut | None:
    """
    Met à jour une catégorie existante.
    Seuls les champs envoyés (non-None) sont modifiés.
    Retourne la catégorie modifiée, ou None si introuvable.
    """
    for cat in _categories:
        if cat["id"] == category_id:
            # model_dump(exclude_unset=True) → ne garde que les champs envoyés
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    cat[key] = value
            return CategoryOut(**cat)
    return None


def delete(category_id: int) -> bool:
    """Supprime une catégorie par son id. Retourne True si supprimée, False sinon."""
    global _categories

    for i, cat in enumerate(_categories):
        if cat["id"] == category_id:
            _categories.pop(i)
            return True
    return False
