"""
Tests pour app.utils.validators

Couvre :
- ProductValidator.validate_price() — cas valides et invalides
"""

import pytest
from app.utils.validators import ProductValidator
from app.core.exceptions import InvalidProductPriceException


class TestProductValidator:
    """Ensemble de tests pour ProductValidator."""

    def test_validate_price_valid_positive(self):
        """Test qu'un prix positif valide passe sans erreur."""
        ProductValidator.validate_price(10.5)
        ProductValidator.validate_price(0.01)
        ProductValidator.validate_price(1000.99)
        # Pas d'assertion nécessaire — pas d'exception levée = succès

    def test_validate_price_zero_raises_exception(self):
        """Test qu'un prix de 0 lève une exception."""
        with pytest.raises(InvalidProductPriceException):
            ProductValidator.validate_price(0)

    def test_validate_price_negative_raises_exception(self):
        """Test qu'un prix négatif lève une exception."""
        with pytest.raises(InvalidProductPriceException):
            ProductValidator.validate_price(-10.5)

    def test_validate_price_exception_message(self):
        """Test que le message d'exception est correct."""
        with pytest.raises(InvalidProductPriceException, match="Price must be greater than 0"):
            ProductValidator.validate_price(-5)
