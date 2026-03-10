"""
Modèles SQLAlchemy — les TABLES de la base de données.

Différence avec les modèles Pydantic :
- Pydantic (models/category.py) → valide les données entrantes/sortantes de l'API
- SQLAlchemy (ici) → définit la structure des tables dans Postgres

Chaque classe = une table. Chaque attribut = une colonne.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class CategoryDB(Base):
    """Table 'categories' dans Postgres."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relation → un catégorie a plusieurs produits (pour US2 - Dania)
    products = relationship("ProductDB", back_populates="category")


class ProductDB(Base):
    """Table 'products' dans Postgres (préparé pour US2 - Dania)."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relation inverse → un produit appartient à une catégorie
    category = relationship("CategoryDB", back_populates="products")


class UserDB(Base):
    """Table 'users' dans Postgres (préparé pour US3 - Manoa et US5 - Gaëlle)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
