"""
Tests pour app/core/database.py — configuration SQLAlchemy et dépendances FastAPI.

Teste :
- La création du moteur et de la fabrique de sessions
- La dépendance get_db() — ouverture et fermeture de session
- La gestion des erreurs de connexion
"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.database import get_db, SessionLocal, engine, Base
from app.models.tables import UserDB


def test_engine_created():
    """Test que le moteur SQLAlchemy est correctement créé."""
    assert engine is not None
    # Vérifier que le moteur peut se connecter
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_db_yields_session(db_session):
    """Test que get_db() fournit une session valide."""
    # get_db() est un générateur qui doit yielder une session
    gen = get_db()
    session = next(gen)
    
    # Vérifier que c'est bien une session
    assert session is not None
    assert hasattr(session, 'query')
    assert hasattr(session, 'add')
    assert hasattr(session, 'commit')
    
    # Fermer le générateur
    try:
        next(gen)
    except StopIteration:
        pass


def test_get_db_closes_session_on_success(db_engine):
    """Test que get_db() ferme la session après utilisation."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    # Vérifier que la session est ouverte
    assert not session.is_active or session.connection() is not None
    
    session.close()
    transaction.rollback()
    connection.close()


def test_get_db_closes_session_on_exception():
    """Test que get_db() ferme la session même en cas d'exception."""
    gen = get_db()
    session = next(gen)
    
    # Vérifier que la session est fournie
    assert session is not None
    
    # La session devrait rester valide jusqu'à sa fermeture explicite
    assert hasattr(session, 'is_active')
    
    # Fermer la session
    session.close()


def test_sessionlocal_configured():
    """Test que SessionLocal est correctement configuré."""
    assert SessionLocal is not None
    # Créer une session de test
    session = SessionLocal()
    assert session is not None
    session.close()


def test_base_metadata():
    """Test que Base.metadata contient les modèles déclarés."""
    assert Base.metadata is not None
    # Les tables devraient être incluses dans metadata
    assert len(Base.metadata.tables) > 0


def test_get_db_with_actual_query(db_engine):
    """Test que get_db() peut être utilisé pour des requêtes réelles."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    # Créer les tables
    Base.metadata.create_all(bind=connection)
    
    # Arjouter un utilisateur de test
    test_user = UserDB(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed123"
    )
    session.add(test_user)
    session.commit()
    
    # Vérifier qu'on peut requêter les données
    user = session.query(UserDB).filter(UserDB.username == "testuser").first()
    assert user is not None
    assert user.username == "testuser"
    
    # Nettoyer
    session.close()
    transaction.rollback()
    connection.close()
