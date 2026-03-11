from sqlalchemy.orm import Session

from app.models.tables import ProductDB
from app.utils.validators import ProductValidator
from app.models.product import ProductCreate, ProductUpdate
from app.repositories.product_repo import ProductRepository


class ProductService:
    """
    Provide business logic for product operations.

    This service acts as an intermediary between the API layer
    and the repository layer, handling product-related operations.
    """

    @staticmethod
    def list_products(db: Session) -> list[ProductDB]:
        """
        Retrieve all available products.
        """
        return ProductRepository.get_all(db)

    @staticmethod
    def filter_products(
        db: Session,
        category_id: int = None,
        min_price: float = None,
        max_price: float = None,
        name: str = None
    ) -> list[ProductDB]:
        """
        Filter products by category, price range, and name.
        """
        return ProductRepository.filter_products(
            db,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            name=name
        )

    @staticmethod
    def create_product(db: Session, data: ProductCreate) -> ProductDB:
        """
        Create a new product.

        Args:
            db: SQLAlchemy database session.
            data: Product creation schema containing validated data.

        Returns:
            Product: The created product instance.
        """
        ProductValidator.validate_price(data.price)

        product = ProductDB(**data.model_dump())

        return ProductRepository.create(db, product)

    @staticmethod
    def delete_product(db: Session, product_id: int) -> ProductDB | None:
        """
        Soft delete a product.

        Args:
            db: SQLAlchemy database session.
            product_id: Identifier of the product to delete.

        Returns:
            Product | None: The deleted product if found,
            otherwise None.
        """
        return ProductRepository.soft_delete(db, product_id)

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        data: ProductUpdate
    ) -> ProductDB | None:
        """
        Update an existing product.

        Args:
            db: SQLAlchemy database session.
            product_id: Identifier of the product to update.
            data: Product update schema containing fields to modify.

        Returns:
            Product | None: The updated product if found,
            otherwise None.
        """

        if data.price is not None:
            ProductValidator.validate_price(data.price)

        return ProductRepository.update(
            db,
            product_id,
            data.model_dump(exclude_unset=True)
        )