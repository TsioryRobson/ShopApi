"""
Tests pour app.services.user_service

Couvre :
- Création d'utilisateur (valide, username dupli., email dupli.)
- Récupération (par ID, tous)
- Mise à jour (champ seul, changement email/username)
- Suppression
"""

import pytest
from fastapi import HTTPException
from app.models.user import UserCreate, UserUpdate
from app.models.tables import UserDB
from app.services import user_service


class TestUserService:
    """Tests de la logique métier utilisateur."""

    def test_get_all_users_empty(self, db_session):
        """Test que get_all_users retourne une liste vide au départ."""
        users = user_service.get_all_users(db_session)
        assert users == []

    def test_create_user_success(self, db_session):
        """Test la création d'un utilisateur valide."""
        data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="securepass123"
        )
        user = user_service.create_user(db_session, data)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        # Le mot de passe ne doit jamais être en réponse
        assert not hasattr(user, 'password')

    def test_create_user_duplicate_username(self, db_session):
        """Test qu'on ne peut pas créer deux utilisateurs avec le même username."""
        data1 = UserCreate(
            username="dupliuser",
            email="user1@example.com",
            password="pass123"
        )
        user_service.create_user(db_session, data1)

        data2 = UserCreate(
            username="dupliuser",
            email="user2@example.com",
            password="pass123"
        )
        with pytest.raises(HTTPException) as exc_info:
            user_service.create_user(db_session, data2)

        assert exc_info.value.status_code == 409
        assert "username" in exc_info.value.detail.lower()

    def test_create_user_duplicate_email(self, db_session):
        """Test qu'on ne peut pas créer deux utilisateurs avec le même email."""
        data1 = UserCreate(
            username="user1",
            email="dupli@example.com",
            password="pass123"
        )
        user_service.create_user(db_session, data1)

        data2 = UserCreate(
            username="user2",
            email="dupli@example.com",
            password="pass123"
        )
        with pytest.raises(HTTPException) as exc_info:
            user_service.create_user(db_session, data2)

        assert exc_info.value.status_code == 409
        assert "email" in exc_info.value.detail.lower()

    def test_get_user_by_id_success(self, db_session):
        """Test la récupération d'un utilisateur sans erreur."""
        data = UserCreate(
            username="alice",
            email="alice@example.com",
            password="pass123"
        )
        created = user_service.create_user(db_session, data)
        retrieved = user_service.get_user(db_session, created.id)

        assert retrieved.id == created.id
        assert retrieved.username == "alice"

    def test_get_user_not_found(self, db_session):
        """Test que récupérer un user inexistant lève 404."""
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_user(db_session, 999)

        assert exc_info.value.status_code == 404

    def test_get_all_users_multiple(self, db_session):
        """Test que get_all_users retourne plusieurs utilisateurs."""
        for i in range(3):
            data = UserCreate(
                username=f"user{i}",
                email=f"user{i}@example.com",
                password="pass123"
            )
            user_service.create_user(db_session, data)

        users = user_service.get_all_users(db_session)
        assert len(users) == 3

    def test_update_user_email_only(self, db_session):
        """Test la mise à jour partielle d'un utilisateur (email seul)."""
        data = UserCreate(
            username="bob",
            email="bob@example.com",
            password="pass123"
        )
        created = user_service.create_user(db_session, data)

        update_data = UserUpdate(email="bob.new@example.com")
        updated = user_service.update_user(db_session, created.id, update_data)

        assert updated.email == "bob.new@example.com"
        assert updated.username == "bob"  # Inchangé

    def test_update_user_password(self, db_session):
        """Test la mise à jour du mot de passe."""
        data = UserCreate(
            username="charlie",
            email="charlie@example.com",
            password="oldpass123"
        )
        created = user_service.create_user(db_session, data)

        update_data = UserUpdate(password="newpass456")
        updated = user_service.update_user(db_session, created.id, update_data)

        # Vérifier que le mot de passe peut être validé avec le nouveau
        from app.core.security import verify_password
        db_user = db_session.query(UserDB).filter(UserDB.id == created.id).first()
        assert verify_password("newpass456", db_user.hashed_password)
        assert not verify_password("oldpass123", db_user.hashed_password)

    def test_update_user_not_found(self, db_session):
        """Test que mettre à jour un user inexistant lève 404."""
        update_data = UserUpdate(email="test@example.com")
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(db_session, 999, update_data)

        assert exc_info.value.status_code == 404

    def test_update_user_duplicate_email(self, db_session):
        """Test qu'on ne peut pas changer deux users vers le même email."""
        data1 = UserCreate(
            username="user1",
            email="email1@example.com",
            password="pass123"
        )
        user1 = user_service.create_user(db_session, data1)

        data2 = UserCreate(
            username="user2",
            email="email2@example.com",
            password="pass123"
        )
        user2 = user_service.create_user(db_session, data2)

        # Essayer d'assigner l'email de user1 à user2
        update_data = UserUpdate(email="email1@example.com")
        with pytest.raises(HTTPException) as exc_info:
            user_service.update_user(db_session, user2.id, update_data)

        assert exc_info.value.status_code == 409

    def test_delete_user_success(self, db_session):
        """Test la suppression d'un utilisateur."""
        data = UserCreate(
            username="deluser",
            email="del@example.com",
            password="pass123"
        )
        created = user_service.create_user(db_session, data)
        result = user_service.delete_user(db_session, created.id)

        assert "supprim" in result["message"].lower()

        # Vérifier que l'utilisateur n'existe plus
        with pytest.raises(HTTPException):
            user_service.get_user(db_session, created.id)

    def test_delete_user_not_found(self, db_session):
        """Test que supprimer un user inexistant lève 404."""
        with pytest.raises(HTTPException) as exc_info:
            user_service.delete_user(db_session, 999)

        assert exc_info.value.status_code == 404
