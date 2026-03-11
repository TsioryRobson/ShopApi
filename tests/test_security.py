"""
Tests pour app.core.security

Couvre :
- hash_password() — hachage avec salt
- verify_password() — vérification du mot de passe
"""

import pytest
from app.core.security import hash_password, verify_password


class TestSecurityFunctions:
    """Tests des fonctions de sécurité."""

    def test_hash_password_creates_different_hashes(self):
        """Test que le même mot de passe génère des hashes différents (cause: salt aléatoire)."""
        password = "securepass123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Les hashes doivent être différents (salt aléatoire)
        assert hash1 != hash2

    def test_hash_password_format(self):
        """Test que le hash a le format 'salt:hash'."""
        hashed = hash_password("test")
        parts = hashed.split(":")
        assert len(parts) == 2
        assert len(parts[0]) == 32  # 16 bytes en hex = 32 caractères
        assert len(parts[1]) == 64  # SHA-256 en hex = 64 caractères

    def test_verify_password_correct(self):
        """Test que verify_password retourne True pour un mot de passe correct."""
        password = "mypassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test que verify_password retourne False pour un mot de passe incorrect."""
        password = "mypassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty_returns_false(self):
        """Test que verify_password avec un hash vide retourne False."""
        assert verify_password("anypassword", "") is False

    def test_verify_password_malformed_hash_returns_false(self):
        """Test que verify_password avec un hash mal formé retourne False."""
        assert verify_password("password", "malformed") is False
        assert verify_password("password", "missing:colon:here") is False

    def test_verify_password_case_sensitive(self):
        """Test que la comparaison des mots de passe est sensible à la casse."""
        password = "MyPassword123"
        hashed = hash_password(password)

        assert verify_password("MyPassword123", hashed) is True
        assert verify_password("mypassword123", hashed) is False
