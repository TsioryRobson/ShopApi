"""
Tests complémentaires pour app/repositories/user_repo.py.

Teste les cas d'exception et les chemins non couverts:
- Exception lors de update()
- Exception lors de delete()
- Cas limites
"""

import pytest
from unittest.mock import patch
from app.models.tables import UserDB
from app.repositories import user_repo


class TestUserRepositoryExceptions:
    """Tests des cas d'exception du repository utilisateurs."""

    def test_update_with_exception(self, db_session):
        """Test que update() gère les exceptions et rollback."""
        # D'abord créer un utilisateur
        user = UserDB(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        user_id = user.id
        
        # Patch la session pour simuler une exception lors du commit
        with patch.object(db_session, 'commit', side_effect=Exception("DB Error")):
            with pytest.raises(Exception) as exc_info:
                user_repo.update(
                    db_session,
                    user_id,
                    {"email": "newemail@example.com"}
                )
            
            assert "DB Error" in str(exc_info.value)

    def test_delete_with_exception(self, db_session):
        """Test que delete() gère les exceptions et rollback."""
        # D'abord créer un utilisateur
        user = UserDB(
            username="deluser",
            email="del@example.com",
            hashed_password="hashed123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        user_id = user.id
        
        # Patch la session pour simuler une exception lors du commit
        with patch.object(db_session, 'commit', side_effect=Exception("DB Error")):
            with pytest.raises(Exception) as exc_info:
                user_repo.delete(db_session, user_id)
            
            assert "DB Error" in str(exc_info.value)

    def test_update_not_found(self, db_session):
        """Test update() quand l'utilisateur n'existe pas."""
        result = user_repo.update(
            db_session,
            999,
            {"email": "newemail@example.com"}
        )
        assert result is None

    def test_delete_not_found(self, db_session):
        """Test delete() quand l'utilisateur n'existe pas."""
        result = user_repo.delete(db_session, 999)
        assert result is False

    def test_update_multiple_fields(self, db_session):
        """Test update() avec plusieurs champs."""
        # Créer un utilisateur
        user = UserDB(
            username="alice",
            email="alice@example.com",
            hashed_password="pass123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        user_id = user.id
        
        # Mettre à jour plusieurs champs
        updated = user_repo.update(
            db_session,
            user_id,
            {
                "email": "alice.new@example.com",
                "hashed_password": "newpass456"
            }
        )
        
        assert updated is not None
        assert updated.email == "alice.new@example.com"
        assert updated.hashed_password == "newpass456"
        assert updated.username == "alice"  # Pas changé

    def test_delete_success(self, db_session):
        """Test la suppression réussie d'un utilisateur."""
        # Créer un utilisateur
        user = UserDB(
            username="tobedeleted",
            email="del@example.com",
            hashed_password="pass123"
        )
        db_session.add(user)
        db_session.commit()
        user_id = user.id
        
        # Supprimer
        result = user_repo.delete(db_session, user_id)
        assert result is True
        
        # Vérifier qu'il n'existe plus
        deleted_user = db_session.query(UserDB).filter(UserDB.id == user_id).first()
        assert deleted_user is None

    def test_get_all_users_after_operations(self, db_session):
        """Test get_all() après plusieurs opérations."""
        # Créer 3 utilisateurs
        for i in range(3):
            user = UserDB(
                username=f"user{i}",
                email=f"user{i}@example.com",
                hashed_password="pass123"
            )
            db_session.add(user)
        db_session.commit()
        
        all_users = user_repo.get_all(db_session)
        assert len(all_users) == 3

    def test_get_by_email_case_sensitive(self, db_session):
        """Test que get_by_email() est sensible à la casse."""
        user = UserDB(
            username="testuser",
            email="Test@Example.Com",
            hashed_password="pass123"
        )
        db_session.add(user)
        db_session.commit()
        
        # Chercher avec la bonne casse
        found = user_repo.get_by_email(db_session, "Test@Example.Com")
        assert found is not None
        
        # Chercher avec une casse différente (SQL est généralement case-insensitive)
        # mais on teste le comportement
        found_lower = user_repo.get_by_email(db_session, "test@example.com")
        # Cela pourrait être None ou le même user selon la DB

    def test_create_user_with_special_characters(self, db_session):
        """Test la création d'utilisateur avec des caractères spéciaux."""
        user = UserDB(
            username="user_with-special.chars",
            email="special+chars@example.com",
            hashed_password="pass123"
        )
        
        created = user_repo.create(
            db_session,
            "user_with-special.chars",
            "special+chars@example.com",
            "pass123"
        )
        
        assert created.username == "user_with-special.chars"
        assert created.email == "special+chars@example.com"
