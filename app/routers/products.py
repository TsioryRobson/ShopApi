from app.models.product import ProductCreate, ProductUpdate, ProductOut
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.product_service import ProductService
from app.core.security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    """
    Retrieve all available products.
    """
    return ProductService.list_products(db)

@router.get("/filter", response_model=list[ProductOut])
def filter_products(
    category_id: int = None,
    min_price: float = None,
    max_price: float = None,
    name: str = None,
    db: Session = Depends(get_db)
):
    """
    Filter products by category, price range, and name.
    """
    return ProductService.filter_products(
        db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        name=name
    )


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
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
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Soft delete a product by its identifier.

    Args:
        product_id: Identifier of the product to delete.
        db: SQLAlchemy database session.
        current_user: The currently authenticated user.

    Raises:
        HTTPException: If the product does not exist.

    Returns:
        dict: Confirmation message indicating the product was deleted.
    """
    product = ProductService.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted"}


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    """
    Update an existing product.

    Args:
        product_id: Identifier of the product to update.
        product: Updated product data.
        db: SQLAlchemy database session.
        current_user: The currently authenticated user.

    Raises:
        HTTPException: If the product does not exist.

    Returns:
        Product: The updated product.
    """
    updated = ProductService.update_product(db, product_id, product)

    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated
