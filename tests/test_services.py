"""
Tests pour les services category et product

Couvre :
- Category : CRUD, unicité du name
- Product : CRUD, validation prix, soft delete
"""

import pytest
from fastapi import HTTPException
from app.models.category import CategoryCreate, CategoryUpdate
from app.models.product import ProductCreate, ProductUpdate
from app.services import category_service
from app.services.product_service import ProductService


class TestCategoryService:
    """Tests de la logique métier catégorie."""

    def test_get_all_categories_empty(self, db_session):
        """Test que get_all_categories retourne une liste vide au départ."""
        categories = category_service.get_all_categories(db_session)
        assert categories == []

    def test_create_category_success(self, db_session):
        """Test la création d'une catégorie valide."""
        data = CategoryCreate(name="Electronics", description="Electronic devices")
        category = category_service.create_category(db_session, data)

        assert category.id is not None
        assert category.name == "Electronics"
        assert category.description == "Electronic devices"

    def test_create_category_name_required(self, db_session):
        """Test que le name est obligatoire."""
        # Ce test est au niveau Pydantic, pas au service
        # On peut tester que Pydantic valide
        with pytest.raises(Exception):  # ValueError ou ValidationError
            CategoryCreate(name="", description="test")

    def test_get_category_by_id(self, db_session):
        """Test la récupération d'une catégorie par ID."""
        data = CategoryCreate(name="Books")
        created = category_service.create_category(db_session, data)
        retrieved = category_service.get_category(db_session, created.id)

        assert retrieved.id == created.id
        assert retrieved.name == "Books"

    def test_get_category_not_found(self, db_session):
        """Test que récupérer une catégorie inexistante lève 404."""
        with pytest.raises(HTTPException) as exc_info:
            category_service.get_category(db_session, 999)

        assert exc_info.value.status_code == 404

    def test_get_all_categories_multiple(self, db_session):
        """Test que get_all_categories retourne plusieurs catégories."""
        for i in range(3):
            data = CategoryCreate(name=f"Category {i}")
            category_service.create_category(db_session, data)

        categories = category_service.get_all_categories(db_session)
        assert len(categories) == 3

    def test_update_category_success(self, db_session):
        """Test la mise à jour d'une catégorie."""
        data = CategoryCreate(name="OldName", description="Old desc")
        created = category_service.create_category(db_session, data)

        update_data = CategoryUpdate(name="NewName", description="New desc")
        updated = category_service.update_category(db_session, created.id, update_data)

        assert updated.name == "NewName"
        assert updated.description == "New desc"

    def test_update_category_partial(self, db_session):
        """Test que la mise à jour partielle fonctionne."""
        data = CategoryCreate(name="Clothing", description="Clothes")
        created = category_service.create_category(db_session, data)

        update_data = CategoryUpdate(description="Updated description only")
        updated = category_service.update_category(db_session, created.id, update_data)

        assert updated.name == "Clothing"  # Inchangé
        assert updated.description == "Updated description only"

    def test_update_category_not_found(self, db_session):
        """Test que mettre à jour une catégorie inexistante lève 404."""
        update_data = CategoryUpdate(name="Test")
        with pytest.raises(HTTPException) as exc_info:
            category_service.update_category(db_session, 999, update_data)

        assert exc_info.value.status_code == 404

    def test_delete_category_success(self, db_session):
        """Test la suppression d'une catégorie."""
        data = CategoryCreate(name="ToDelete")
        created = category_service.create_category(db_session, data)

        result = category_service.delete_category(db_session, created.id)
        assert "supprim" in result["message"].lower()

        # Vérifier que la catégorie n'existe plus
        with pytest.raises(HTTPException):
            category_service.get_category(db_session, created.id)

    def test_delete_category_not_found(self, db_session):
        """Test que supprimer une catégorie inexistante lève 404."""
        with pytest.raises(HTTPException) as exc_info:
            category_service.delete_category(db_session, 999)

        assert exc_info.value.status_code == 404


class TestProductService:
    """Tests de la logique métier produit."""

    @pytest.fixture
    def category(self, db_session):
        """Crée une catégorie de test."""
        data = CategoryCreate(name="TestCategory")
        return category_service.create_category(db_session, data)

    def test_list_products_empty(self, db_session):
        """Test que list_products retourne une liste vide au départ."""
        products = ProductService.list_products(db_session)
        assert products == []

    def test_create_product_success(self, db_session, category):
        """Test la création d'un produit valide."""
        data = ProductCreate(name="Laptop", price=999.99, category_id=category.id)
        product = ProductService.create_product(db_session, data)

        assert product.id is not None
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.category_id == category.id
        assert product.status == 10  # Actif par défaut

    def test_create_product_invalid_price_zero(self, db_session, category):
        """Test qu'un prix de 0 lève une exception (Pydantic)."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ProductCreate(name="InvalidProduct", price=0, category_id=category.id)

    def test_create_product_invalid_price_negative(self, db_session, category):
        """Test qu'un prix négatif lève une exception (Pydantic)."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ProductCreate(name="InvalidProduct", price=-50, category_id=category.id)

    def test_list_products_active_only(self, db_session, category):
        """Test que list_products ne retourne que les produits actifs (status != 1)."""
        # Créer 2 produits
        for i in range(2):
            data = ProductCreate(
                name=f"Product {i}", price=10.0, category_id=category.id
            )
            ProductService.create_product(db_session, data)

        # Tous les produits devraient être listés (status = 10 par défaut)
        products = ProductService.list_products(db_session)
        assert len(products) == 2

    def test_update_product_success(self, db_session, category):
        """Test la mise à jour d'un produit."""
        data = ProductCreate(name="OldName", price=50.0, category_id=category.id)
        created = ProductService.create_product(db_session, data)

        update_data = ProductUpdate(name="NewName", price=75.0)
        updated = ProductService.update_product(db_session, created.id, update_data)

        assert updated.name == "NewName"
        assert updated.price == 75.0

    def test_update_product_partial(self, db_session, category):
        """Test que la mise à jour partielle fonctionne."""
        data = ProductCreate(name="Phone", price=500.0, category_id=category.id)
        created = ProductService.create_product(db_session, data)

        update_data = ProductUpdate(price=450.0)
        updated = ProductService.update_product(db_session, created.id, update_data)

        assert updated.name == "Phone"  # Inchangé
        assert updated.price == 450.0

    def test_update_product_not_found(self, db_session):
        """Test que mettre à jour un produit inexistant retourne None."""
        update_data = ProductUpdate(name="Test")
        result = ProductService.update_product(db_session, 999, update_data)

        assert result is None

    def test_delete_product_soft_delete(self, db_session, category):
        """Test que la suppression est un soft delete (status = 1)."""
        data = ProductCreate(name="ToDelete", price=50.0, category_id=category.id)
        created = ProductService.create_product(db_session, data)

        result = ProductService.delete_product(db_session, created.id)
        assert result is not None
        assert result.status == 1  # Marqué comme supprimé

        # Vérifier que list_products ne le retourne plus
        products = ProductService.list_products(db_session)
        assert created.id not in [p.id for p in products]

    def test_delete_product_not_found(self, db_session):
        """Test que supprimer un produit inexistant retourne None."""
        result = ProductService.delete_product(db_session, 999)
        assert result is None

    def test_get_product_by_id_success(self, db_session, category):
        """Test la récupération d'un produit existant par ID."""
        created = ProductService.create_product(
            db_session,
            ProductCreate(name="Monitor", price=120.0, category_id=category.id),
        )

        found = ProductService.get_product(db_session, created.id)
        assert found is not None
        assert found.id == created.id
        assert found.name == "Monitor"

    # ------------------------------------------------------------------
    # Tests for new filter functionality
    # ------------------------------------------------------------------
    def test_filter_products_by_category(self, db_session, category):
        """Filtering should return only products of given category."""
        # create another category
        from app.services import category_service

        other = category_service.create_category(
            db_session, CategoryCreate(name="Other")
        )
        # create products in both categories
        ProductService.create_product(
            db_session, ProductCreate(name="A", price=5.0, category_id=category.id)
        )
        ProductService.create_product(
            db_session, ProductCreate(name="B", price=7.0, category_id=other.id)
        )

        results = ProductService.filter_products(db_session, category_id=category.id)
        assert len(results) == 1
        assert results[0].category_id == category.id

    def test_filter_products_by_price_range(self, db_session, category):
        """Filtering should respect min_price/max_price bounds."""
        ProductService.create_product(
            db_session, ProductCreate(name="Cheap", price=10.0, category_id=category.id)
        )
        ProductService.create_product(
            db_session, ProductCreate(name="Mid", price=50.0, category_id=category.id)
        )
        ProductService.create_product(
            db_session,
            ProductCreate(name="Expensive", price=100.0, category_id=category.id),
        )

        res = ProductService.filter_products(db_session, min_price=20, max_price=80)
        prices = [p.price for p in res]
        assert prices == [50.0]

    def test_filter_products_by_name(self, db_session, category):
        """Filtering by partial name should perform case‑insensitive match."""
        ProductService.create_product(
            db_session,
            ProductCreate(name="FirstItem", price=1, category_id=category.id),
        )
        ProductService.create_product(
            db_session, ProductCreate(name="Second", price=2, category_id=category.id)
        )

        res = ProductService.filter_products(db_session, name="first")
        assert len(res) == 1
        assert "FirstItem" in res[0].name

    def test_filter_products_combined(self, db_session, category):
        """Combining filters should narrow results accordingly."""
        ProductService.create_product(
            db_session, ProductCreate(name="Combo", price=30.0, category_id=category.id)
        )
        ProductService.create_product(
            db_session, ProductCreate(name="Combo", price=70.0, category_id=category.id)
        )

        res = ProductService.filter_products(
            db_session, min_price=20, max_price=50, name="combo"
        )
        assert len(res) == 1
        assert res[0].price == 30.0
