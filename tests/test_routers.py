"""
Tests d'intégration pour les routers HTTP

Couvre :
- Endpoints /users/ (CRUD complet)
- Endpoints /categories/ (CRUD complet)
- Endpoints /products/ (CRUD complet)
- Codes d'erreur et validations
"""

import pytest
from fastapi import status


class TestUsersRouter:
    """Tests des endpoints /users/"""

    def test_list_users_empty(self, client):
        """GET /users/ — liste vide au départ."""
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_user(self, client):
        """POST /users/ — créer un utilisateur."""
        response = client.post(
            "/users/",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "securepass123"
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "password" not in data
        assert "id" in data

    def test_create_user_duplicate_username(self, client):
        """POST /users/ — 409 si username déjà utilisé."""
        client.post(
            "/users/",
            json={
                "username": "duplicate",
                "email": "email1@example.com",
                "password": "pass123"
            }
        )
        response = client.post(
            "/users/",
            json={
                "username": "duplicate",
                "email": "email2@example.com",
                "password": "pass123"
            }
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_create_user_duplicate_email(self, client):
        """POST /users/ — 409 si email déjà utilisé."""
        client.post(
            "/users/",
            json={
                "username": "user1",
                "email": "duplicate@example.com",
                "password": "pass123"
            }
        )
        response = client.post(
            "/users/",
            json={
                "username": "user2",
                "email": "duplicate@example.com",
                "password": "pass123"
            }
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_get_user_by_id(self, client):
        """GET /users/{id} — récupérer un utilisateur."""
        # Créer un user
        create_response = client.post(
            "/users/",
            json={
                "username": "alice",
                "email": "alice@example.com",
                "password": "pass123"
            }
        )
        user_id = create_response.json()["id"]

        # Récupérer le user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "alice"

    def test_get_user_not_found(self, client):
        """GET /users/{id} — 404 si user inexistant."""
        response = client.get("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_users_multiple(self, client):
        """GET /users/ — lister plusieurs utilisateurs."""
        for i in range(3):
            client.post(
                "/users/",
                json={
                    "username": f"user{i}",
                    "email": f"user{i}@example.com",
                    "password": "pass123"
                }
            )

        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    def test_update_user(self, client):
        """PUT /users/{id} — mettre à jour un utilisateur."""
        create_response = client.post(
            "/users/",
            json={
                "username": "bob",
                "email": "bob@example.com",
                "password": "pass123"
            }
        )
        user_id = create_response.json()["id"]

        response = client.put(
            f"/users/{user_id}",
            json={"email": "bob.new@example.com"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "bob.new@example.com"
        assert data["username"] == "bob"

    def test_update_user_not_found(self, client):
        """PUT /users/{id} — 404 si user inexistant."""
        response = client.put(
            "/users/999",
            json={"email": "test@example.com"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user(self, client):
        """DELETE /users/{id} — supprimer un utilisateur."""
        create_response = client.post(
            "/users/",
            json={
                "username": "todelete",
                "email": "delete@example.com",
                "password": "pass123"
            }
        )
        user_id = create_response.json()["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == status.HTTP_200_OK
        assert "supprim" in response.json()["message"].lower()

        # Vérifier qu'il n'existe plus
        response = client.get(f"/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_user_not_found(self, client):
        """DELETE /users/{id} — 404 si user inexistant."""
        response = client.delete("/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCategoriesRouter:
    """Tests des endpoints /categories/"""

    def test_list_categories_empty(self, client):
        """GET /categories/ — liste vide au départ."""
        response = client.get("/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_category(self, client):
        """POST /categories/ — créer une catégorie."""
        response = client.post(
            "/categories/",
            json={"name": "Electronics", "description": "Electric devices"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Electronics"
        assert "id" in data

    def test_get_category_by_id(self, client):
        """GET /categories/{id} — récupérer une catégorie."""
        create_response = client.post(
            "/categories/",
            json={"name": "Books"}
        )
        category_id = create_response.json()["id"]

        response = client.get(f"/categories/{category_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Books"

    def test_get_category_not_found(self, client):
        """GET /categories/{id} — 404 si catégorie inexistante."""
        response = client.get("/categories/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_category(self, client):
        """PUT /categories/{id} — mettre à jour une catégorie."""
        create_response = client.post(
            "/categories/",
            json={"name": "OldName"}
        )
        category_id = create_response.json()["id"]

        response = client.put(
            f"/categories/{category_id}",
            json={"name": "NewName"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "NewName"

    def test_delete_category(self, client):
        """DELETE /categories/{id} — supprimer une catégorie."""
        create_response = client.post(
            "/categories/",
            json={"name": "ToDelete"}
        )
        category_id = create_response.json()["id"]

        response = client.delete(f"/categories/{category_id}")
        assert response.status_code == status.HTTP_200_OK

        # Vérifier qu'elle n'existe plus
        response = client.get(f"/categories/{category_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestProductsRouter:
    """Tests des endpoints /products/"""

    @pytest.fixture
    def category_id(self, client):
        """Crée une catégorie et retourne son ID pour les tests."""
        response = client.post(
            "/categories/",
            json={"name": "TestCategory"}
        )
        return response.json()["id"]

    def test_list_products_empty(self, client):
        """GET /products/ — liste vide au départ."""
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_create_product(self, client, category_id):
        """POST /products/ — créer un produit."""
        response = client.post(
            "/products/",
            json={"name": "Laptop", "price": 999.99, "category_id": category_id}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Laptop"
        assert data["price"] == 999.99
        assert "id" in data

    def test_create_product_invalid_price_zero(self, client, category_id):
        """POST /products/ — erreur si prix = 0."""
        response = client.post(
            "/products/",
            json={"name": "InvalidProduct", "price": 0, "category_id": category_id}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY or \
               response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_create_product_invalid_price_negative(self, client, category_id):
        """POST /products/ — erreur si prix < 0."""
        response = client.post(
            "/products/",
            json={"name": "InvalidProduct", "price": -50, "category_id": category_id}
        )
        # Pydantic rejette le prix négatif (gt=0)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_update_product(self, client, category_id):
        """PUT /products/{id} — mettre à jour un produit."""
        create_response = client.post(
            "/products/",
            json={"name": "Phone", "price": 500.0, "category_id": category_id}
        )
        product_id = create_response.json()["id"]

        response = client.put(
            f"/products/{product_id}",
            json={"price": 450.0}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["price"] == 450.0

    def test_update_product_not_found(self, client):
        """PUT /products/{id} — 404 si produit inexistant."""
        response = client.put(
            "/products/999",
            json={"name": "Test"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_product_soft_delete(self, client, category_id):
        """DELETE /products/{id} — soft delete (produit toujours en DB)."""
        create_response = client.post(
            "/products/",
            json={"name": "ToDelete", "price": 50.0, "category_id": category_id}
        )
        product_id = create_response.json()["id"]

        response = client.delete(f"/products/{product_id}")
        assert response.status_code == status.HTTP_200_OK

        # Vérifier qu'il n'est plus dans la liste (soft delete)
        response = client.get("/products/")
        product_ids = [p.get("id") for p in response.json()]
        assert product_id not in product_ids

    def test_delete_product_not_found(self, client):
        """DELETE /products/{id} — 404 si produit inexistant."""
        response = client.delete("/products/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_products_multiple(self, client, category_id):
        """GET /products/ — lister plusieurs produits."""
        for i in range(3):
            client.post(
                "/products/",
                json={
                    "name": f"Product {i}",
                    "price": float(i + 1) * 10,
                    "category_id": category_id
                }
            )

        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 3

    def test_filter_products_router(self, client, category_id):
        """GET /products/filter avec différents paramètres."""
        # create a few products
        client.post("/products/", json={"name": "Apple", "price": 5.0, "category_id": category_id})
        client.post("/products/", json={"name": "Banana", "price": 15.0, "category_id": category_id})
        client.post("/products/", json={"name": "Cherry", "price": 25.0, "category_id": category_id})

        # filter by min_price only
        resp = client.get(f"/products/filter?min_price=10")
        assert resp.status_code == status.HTTP_200_OK
        assert all(p["price"] >= 10 for p in resp.json())

        # filter by name substring
        resp2 = client.get(f"/products/filter?name=app")
        assert resp2.status_code == status.HTTP_200_OK
        assert len(resp2.json()) == 1
        assert resp2.json()[0]["name"] == "Apple"

        # filter by range and name
        resp3 = client.get(f"/products/filter?min_price=10&max_price=30&name=an")
        assert resp3.status_code == status.HTTP_200_OK
        assert len(resp3.json()) == 1
        assert resp3.json()[0]["name"] == "Banana"
