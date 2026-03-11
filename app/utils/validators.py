from app.core.exceptions import InvalidProductPriceException


class ProductValidator:
    """
    Provide validation utilities for product-related data.
    """

    @staticmethod
    def validate_price(price: float):
        """
        Validate that the product price is greater than zero.

        Args:
            price: Price of the product.

        Raises:
            InvalidProductPriceException: If the price is less than or equal to zero.
        """
        if price <= 0:
            raise InvalidProductPriceException("Price must be greater than 0")
