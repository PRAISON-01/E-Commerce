from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session
from starlette import status

from app.config.dependencies import get_session
from app.models.product import Product, AddProduct, UpdateProduct
from app.repositories.product_repository import ProductRepository
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory_service"])

def get_inventory_service(session : Session = Depends(get_session)) -> InventoryService:
    product_repository = ProductRepository(session)
    return InventoryService(repository=product_repository)

class InventoryUpdateRequest(BaseModel):
    product_id : UUID
    quantity: int = Field(gt=0)

@router.post("/create_product", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_new_product(
        payload: AddProduct,
        session : Session = Depends(get_session),
):

    try:
        product_repository = ProductRepository(session)
        new_product = Product(
            name=payload.name,
            description=payload.description,
            price=payload.price,
            quantity=payload.quantity
        )

        return product_repository.save(new_product)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create new catalog product: {str(e)}")


