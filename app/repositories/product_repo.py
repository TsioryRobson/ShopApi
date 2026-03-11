from sqlalchemy.orm import Session

from app.models.tables import ProductDB

class ProductRepository:
    """
    Provide database operations for Product entities.

    This repository handles CRUD operations and soft deletion
    for products using a SQLAlchemy session.
    """

    @staticmethod
    def get_all(db: Session) -> list[ProductDB]:
        """
        Retrieve all active products.

        Args:
            db: SQLAlchemy database session.

        Returns:
            list[Product]: List of products whose status is not deleted.
        """
        return db.query(ProductDB).filter(ProductDB.status != 1).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> ProductDB | None:
        """
        Retrieve a product by its ID.

        Args:
            db: SQLAlchemy database session.
            product_id: ID of the product to retrieve.

        Returns:
            ProductDB | None: The requested product or None if not found.
        """
        return db.query(ProductDB).filter(
            ProductDB.id == product_id,
            ProductDB.status != 1
        ).first()

    @staticmethod
    def create(db: Session, product: ProductDB) -> ProductDB:
        """
        Create a new product in the database.

        Args:
            db: SQLAlchemy database session.
            product: Product instance to persist.

        Returns:
            ProductDB: The created product.
        """
        try:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def soft_delete(db: Session, product_id: int) -> ProductDB | None:
        """
        Soft delete a product by updating its status.

        Args:
            db: SQLAlchemy database session.
            product_id: Identifier of the product to delete.

        Returns:
            ProductDB | None: The updated product if it exists,
            otherwise None.
        """
        product = db.query(ProductDB).filter(ProductDB.id == product_id).first()

        if product is None:
            return None

        try:
            product.status = 1
            db.commit()
            db.refresh(product)
            return product
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def update(db: Session, product_id: int, data: dict) -> ProductDB | None:
        """
        Update an existing product with the provided data.

        Args:
            db: SQLAlchemy database session.
            product_id: Identifier of the product to update.
            data: Dictionary containing fields to update.

        Returns:
            ProductDB | None: The updated product if it exists,
            otherwise None.
        """
        product = db.query(ProductDB).filter(
            ProductDB.id == product_id,
            ProductDB.status != 1
        ).first()

        if product is None:
            return None

        for key, value in data.items():
            setattr(product, key, value)

        try:
            db.commit()
            db.refresh(product)
            return product
        except Exception:
            db.rollback()
            raise