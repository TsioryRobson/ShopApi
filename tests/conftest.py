"""
Fixtures partagées pour tous les tests Pytest.

Configuration :
- Base SQLite en mémoire (pas de dépendance externe)
- Session DB injectée dans l'app FastAPI
- TestClient pour tester les endpoints
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Important: forcer SQLite AVANT d'importer l'application.
# Sans ça, app.core.database tente d'initialiser Postgres au chargement,
# ce qui exige psycopg2 durant la phase de collecte pytest.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.main import app
from app.core.database import get_db
from app.models.tables import Base


@pytest.fixture(scope="session")
def db_engine():
    """Crée un moteur SQLAlchemy avec une DB SQLite en mémoire."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Crée une session DB pour chaque test, isolation garantie par rollback."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Crée un TestClient FastAPI avec la session DB en test injectée."""

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
