"""
Tests complémentaires pour couvrir les cas limites et chemins non couverts.
"""

import pytest
from fastapi import HTTPException
from app.models.user import UserCreate, UserUpdate
from app.services import user_service
from app.core.security import verify_password
from app.models.tables import UserDB


class TestUserServiceAdvanced:
    """Tests avancés pour les cas limites de user_service."""

    def test_update_user_password_and_email(self, db_session):
        """Test la mise à jour du mot de passe ET de l'email simultanément."""
        # Créer un utilisateur
        data = UserCreate(
            username="david", email="david@example.com", password="oldpass123"
        )
        created = user_service.create_user(db_session, data)

        # Mettre à jour le mot de passe ET l'email
        update_data = UserUpdate(email="david.new@example.com", password="newpass456")
        updated = user_service.update_user(db_session, created.id, update_data)

        # Vérifier les modifications
        assert updated.email == "david.new@example.com"
        assert updated.username == "david"  # Inchangé

        # Vérifier que le mot de passe a été changé
        db_user = db_session.query(UserDB).filter(UserDB.id == created.id).first()
        assert verify_password("newpass456", db_user.hashed_password)
        assert not verify_password("oldpass123", db_user.hashed_password)

    def test_update_user_username_and_password(self, db_session):
        """Test la mise à jour du username ET du mot de passe."""
        # Créer un utilisateur
        data = UserCreate(username="eve", email="eve@example.com", password="pass123")
        created = user_service.create_user(db_session, data)

        # Mettre à jour username et password
        update_data = UserUpdate(username="eve_new", password="newpass789")
        updated = user_service.update_user(db_session, created.id, update_data)

        assert updated.username == "eve_new"

        # Vérifier le mot de passe
        db_user = db_session.query(UserDB).filter(UserDB.id == created.id).first()
        assert verify_password("newpass789", db_user.hashed_password)

    def test_update_user_only_password(self, db_session):
        """Test la mise à jour UNIQUEMENT du mot de passe."""
        # Créer un utilisateur
        data = UserCreate(
            username="frank", email="frank@example.com", password="pass123"
        )
        created = user_service.create_user(db_session, data)

        # Mettre à jour UNIQUEMENT le mot de passe
        update_data = UserUpdate(password="brandnew456")
        updated = user_service.update_user(db_session, created.id, update_data)

        # Vérifier que les autres champs restent inchangés
        assert updated.username == "frank"
        assert updated.email == "frank@example.com"

        # Vérifier le nouveau mot de passe
        db_user = db_session.query(UserDB).filter(UserDB.id == created.id).first()
        assert verify_password("brandnew456", db_user.hashed_password)

    def test_update_user_keep_same_username(self, db_session):
        """Test que mettre à jour avec le même username ne cause pas de conflit."""
        # Créer un utilisateur
        data = UserCreate(
            username="grace", email="grace@example.com", password="pass123"
        )
        created = user_service.create_user(db_session, data)

        # Mettre à jour sans changer le username
        update_data = UserUpdate(
            username="grace", email="grace.new@example.com"  # Le même
        )
        updated = user_service.update_user(db_session, created.id, update_data)

        assert updated.username == "grace"
        assert updated.email == "grace.new@example.com"

    def test_update_user_keep_same_email(self, db_session):
        """Test que mettre à jour avec le même email ne cause pas de conflit."""
        # Créer un utilisateur
        data = UserCreate(
            username="henry", email="henry@example.com", password="pass123"
        )
        created = user_service.create_user(db_session, data)

        # Mettre à jour sans changer l'email
        update_data = UserUpdate(
            username="henry_new", email="henry@example.com"  # Le même
        )
        updated = user_service.update_user(db_session, created.id, update_data)

        assert updated.email == "henry@example.com"
        assert updated.username == "henry_new"

    def test_update_user_empty_params_no_change(self, db_session):
        """Test que donner des params vides ne change rien."""
        # Créer un utilisateur
        data = UserCreate(username="iris", email="iris@example.com", password="pass123")
        created = user_service.create_user(db_session, data)

        # Mettre à jour avec les params None
        update_data = UserUpdate()
        updated = user_service.update_user(db_session, created.id, update_data)

        # Rien ne devrait changer
        assert updated.username == "iris"
        assert updated.email == "iris@example.com"

        # Le mot de passe devrait rester le même
        db_user = db_session.query(UserDB).filter(UserDB.id == created.id).first()
        assert verify_password("pass123", db_user.hashed_password)

    def test_update_user_multiple_duplicate_username_error(self, db_session):
        """Test qu'on ne peut pas assigner le username d'un autre utilisateur."""
        # Créer deux utilisateurs
        data1 = UserCreate(
            username="jack", email="jack@example.com", password="pass123"
        )
        user_service.create_user(db_session, data1)

        data2 = UserCreate(
            username="jill", email="jill@example.com", password="pass123"
        )
        user2 = user_service.create_user(db_session, data2)

        # Essayer d'assigner le username de user1 à user2
        update_data = UserUpdate(username="jack")
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(db_session, user2.id, update_data)

        assert exc_info.value.status_code == 409
        assert "username" in exc_info.value.detail.lower()

    def test_delete_user_then_search_not_found(self, db_session):
        """Test qu'après suppression, l'utilisateur est introuvable."""
        # Créer et supprimer
        data = UserCreate(username="kate", email="kate@example.com", password="pass123")
        created = user_service.create_user(db_session, data)
        user_service.delete_user(db_session, created.id)

        # Rechercher doit lever 404
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_user(db_session, created.id)

        assert exc_info.value.status_code == 404
