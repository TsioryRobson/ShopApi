from app.models.product import ProductCreate, ProductUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def list_products(db: Session = Depends(get_db)):
    """
    Retrieve all available products.

    Args:
        db: SQLAlchemy database session provided by dependency injection.

    Returns:
        list: A list of active products.
    """
    return ProductService.list_products(db)


@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product.

    Args:
        product: Product data used to create a new product.
        db: SQLAlchemy database session.

    Returns:
        Product: The created product.
    """
    return ProductService.create_product(db, product)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a product by its identifier.

    Args:
        product_id: Identifier of the product to delete.
        db: SQLAlchemy database session.

    Raises:
        HTTPException: If the product does not exist.

    Returns:
        dict: Confirmation message indicating the product was deleted.
    """
    product = ProductService.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted"}


@router.put("/{product_id}")
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing product.

    Args:
        product_id: Identifier of the product to update.
        product: Updated product data.
        db: SQLAlchemy database session.

    Raises:
        HTTPException: If the product does not exist.

    Returns:
        Product: The updated product.
    """
    updated = ProductService.update_product(db, product_id, product)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated
