from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session
from sqlmodel.orm import session
from starlette import status

from app.config.dependencies import get_session
from app.models.product import Product, AddProduct, UpdateProduct
from app.repositories.product_repository import ProductRepository
from app.services.inventory_service import InventoryService
# from app.repositories import product_repository
# from app.repositories.customer_repository import CustomerRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository

router = APIRouter(prefix="/inventory", tags=["inventory_service"])



def get_inventory_service(session : Session = Depends(get_session)) -> InventoryService:
    product_repository = ProductRepository(session)
    store_keeper_repository = StoreKeeperRepository(session)
    return InventoryService(repository=product_repository, user_repository=store_keeper_repository)

class InventoryUpdateRequest(BaseModel):
    id : UUID
    quantity: int = Field(gt=0)




@router.post("/create_product", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_new_product(
    payload: AddProduct,
    inventory_service: InventoryService = Depends(get_inventory_service),
):
    try:
        return inventory_service.add_product(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )


@router.post("/update_product", response_model=Product, status_code=status.HTTP_202_ACCEPTED)
def update_product(
        payload : UpdateProduct,
        inventory_service : InventoryService = Depends(get_inventory_service),
):
    try:
        return inventory_service.restock(payload)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to restock/update product: {str(e)}")


@router.get("/get_all_products", response_model=list[Product], status_code=status.HTTP_202_ACCEPTED)

def get_all_products(
        store_keeper_id: UUID,
        inventory_service: InventoryService = Depends(get_inventory_service)
):
    try:
        return inventory_service.get_all_products(store_keeper_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get all products: {str(e)}"
        )




@router.get("/get_product", response_model=Product, status_code=status.HTTP_202_ACCEPTED)

def get_product(
        id : UUID,
        store_keeper_id: UUID,
        inventory_service: InventoryService = Depends(get_inventory_service)
):
    try:
        return inventory_service.get_product(id, store_keeper_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get all products: {str(e)}"
        )


@router.delete("/delete_product/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
        id : UUID,
        store_keeper_id : UUID,
        inventory_service : InventoryService = Depends(get_inventory_service),
):
    try:
        return inventory_service.delete(id, store_keeper_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete product: {str(e)}"
        )

