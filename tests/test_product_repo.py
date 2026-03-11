"""
Tests complémentaires pour app/repositories/product_repo.py.

Teste les cas d'exception et les chemins d'erreur non couverts:
- Exception lors de create()
- Exception lors de soft_delete()
- Exception lors de update()
"""

import pytest
from unittest.mock import patch
from app.models.tables import ProductDB
from app.repositories.product_repo import ProductRepository


class TestProductRepositoryExceptions:
    """Tests des cas d'exception du repository produits."""

    def test_create_with_exception(self, db_session):
        """Test que create() gère les exceptions et rollback."""
        product = ProductDB(name="Test Product", price=10.0, category_id=1, status=0)

        # Patch la session pour simuler une exception
        with patch.object(db_session, "commit", side_effect=Exception("DB Error")):
            with pytest.raises(Exception) as exc_info:
                ProductRepository.create(db_session, product)

            assert "DB Error" in str(exc_info.value)

    def test_soft_delete_with_exception(self, db_session):
        """Test que soft_delete() gère les exceptions et rollback."""
        # D'abord créer un produit
        product = ProductDB(name="Delete Test", price=20.0, category_id=1, status=0)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        product_id = product.id

        # Patch la session pour simuler une exception lors du commit
        with patch.object(db_session, "commit", side_effect=Exception("DB Error")):
            with pytest.raises(Exception) as exc_info:
                ProductRepository.soft_delete(db_session, product_id)

            assert "DB Error" in str(exc_info.value)

    def test_update_with_exception(self, db_session):
        """Test que update() gère les exceptions et rollback."""
        # D'abord créer un produit
        product = ProductDB(name="Update Test", price=30.0, category_id=1, status=0)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        product_id = product.id

        # Patch la session pour simuler une exception lors du commit
        with patch.object(db_session, "commit", side_effect=Exception("DB Error")):
            with pytest.raises(Exception) as exc_info:
                ProductRepository.update(db_session, product_id, {"price": 50.0})

            assert "DB Error" in str(exc_info.value)

    def test_soft_delete_not_found(self, db_session):
        """Test soft_delete() quand le produit n'existe pas."""
        result = ProductRepository.soft_delete(db_session, 999)
        assert result is None

    def test_update_not_found(self, db_session):
        """Test update() quand le produit n'existe pas."""
        result = ProductRepository.update(db_session, 999, {"price": 50.0})
        assert result is None

    def test_get_by_id_with_deleted_product(self, db_session):
        """Test que get_by_id() ignore les produits supprimés."""
        # Créer un produit
        product = ProductDB(name="Test", price=10.0, category_id=1, status=0)
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        product_id = product.id

        # Le soft-delete (status=1)
        product.status = 1
        db_session.commit()

        # get_by_id() ne doit pas le retourner
        result = ProductRepository.get_by_id(db_session, product_id)
        assert result is None

    def test_filter_products_all_filters(self, db_session):
        """Test filter_products() avec tous les filtres actifs."""
        # Créer plusieurs produits
        for i in range(3):
            product = ProductDB(
                name=f"Product {i}",
                price=10.0 + i * 5,
                category_id=1 if i < 2 else 2,
                status=0,
            )
            db_session.add(product)
        db_session.commit()

        # Filtrer avec tous les critères
        results = ProductRepository.filter_products(
            db_session, category_id=1, min_price=8.0, max_price=18.0, name="Product"
        )

        assert len(results) >= 1

    def test_filter_products_empty_filters(self, db_session):
        """Test filter_products() sans filtres retourne tous les produits."""
        # Créer un produit
        product = ProductDB(name="Test", price=10.0, category_id=1, status=0)
        db_session.add(product)
        db_session.commit()

        results = ProductRepository.filter_products(db_session)
        assert len(results) >= 1

    def test_create_multiple_products(self, db_session):
        """Test la création de plusieurs produits."""
        for i in range(3):
            product = ProductDB(
                name=f"Product {i}", price=float(10 + i), category_id=1, status=0
            )
            ProductRepository.create(db_session, product)

        all_products = ProductRepository.get_all(db_session)
        assert len(all_products) == 3
