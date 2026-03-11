"""
Tests pour la lifespan et la configuration de démarrage de app/main.py.
"""


def test_app_configuration():
    """Test que l'app FastAPI est correctement configurée."""
    from app.main import app

    assert app.title == "ShopAPI"
    assert app.version == "0.1.0"
    assert (
        "gestion d'inventaire" in app.description.lower()
        or "inventaire" in app.description.lower()
    )

    # Vérifier que les routers sont attachés
    routes = [route.path for route in app.routes]
    assert any("categor" in path for path in routes)
    assert any("product" in path for path in routes)
    assert any("user" in path for path in routes)


def test_cors_origins_parsing():
    """Test que les origines CORS sont correctement parsées."""
    from app.main import cors_origins

    # Les origines CORS devraient être une liste (peut être vide)
    assert isinstance(cors_origins, list)


def test_app_startup_with_missing_db(client):
    """Test que l'app démarre et les endpoints fonctionnent."""
    # La route root devrait fonctionner
    response = client.get("/")
    assert response.status_code == 200


def test_docs_endpoints_available(client):
    """Test que les endpoints de documentation sont disponibles."""
    # OpenAPI docs
    response = client.get("/docs")
    assert response.status_code == 200

    # ReDoc
    response = client.get("/redoc")
    assert response.status_code == 200


def test_app_health_check(client):
    """Test l'endpoint health check de l'API."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Test shop API running"
