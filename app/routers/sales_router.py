from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.config.dependencies import get_session
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.cart_repository import CartRepository
from app.models.order import CreateOrder, OrderResponse, Order
from app.services.sales_service import OrderService
from app.repositories import product_repository, storekeeper_repository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.services import inventory_service
from app.services.cart_service import CartService
from app.services.inventory_service import InventoryService
from app.services.sales_service import OrderService

router = APIRouter(prefix="/sales", tags=["sales"])


def get_sales_service(session: Session = Depends(get_session)) -> OrderService:
    order_repository = OrderRepository(session)
    cart_repository = CartRepository(session)
    product_repo = ProductRepository(session)
    storekeeper_repo = StoreKeeperRepository(session)
    return OrderService(order_repository, cart_repository, product_repo, InventoryService(product_repo, storekeeper_repo))

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
        payload: CreateOrder,
        sales_service: OrderService = Depends(get_sales_service)):
    try:
        return sales_service.create_order(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
        order_id: UUID,
        customer_id: UUID,
        sales_service: OrderService = Depends(get_sales_service)):
    try:
        return sales_service.get_order(customer_id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/customers/{customer_id}/orders", response_model=List[Order])
def list_customer_orders(customer_id: UUID, sales_service: OrderService = Depends(get_sales_service)):
    return sales_service.list_orders(customer_id)


@router.post("/orders/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
        order_id: UUID,
        customer_id: UUID,
        sales_service: OrderService = Depends(get_sales_service)):
    try:
        return sales_service.cancel_order(customer_id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
