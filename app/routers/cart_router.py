from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from starlette import status

from app.models.cart import CreateCart, Cart
from app.repositories import product_repository
from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository
from app.services.cart_service import CartService
from app.config.dependencies import get_session

router = APIRouter(prefix="/cart-service", tags=["cart-service"])

def get_cart_service(session : Session= Depends(get_session)) -> CartService:
    cart_repo = CartRepository(session)
    product_repo = ProductRepository(session)
    return CartService(cart_repo, product_repo)


@router.post("/add_product_to_cart", response_model=Cart, status_code=status.HTTP_201_CREATED)
def add_to_cart(
        customer_id : UUID,
        payload: CreateCart ,
        cart_service : CartService = Depends(get_cart_service)
        ):
    try:
        return cart_service.add_item_to_cart(customer_id , payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/find_cart", response_model=Cart, status_code=status.HTTP_200_OK)
def get_cart(
        customer_id : UUID,
        cart_service : CartService = Depends(get_cart_service)
):
    try:
        return cart_service.get_cart(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/remove_cart", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart(
        customer_id : UUID,
        cart_id : UUID,
        cart_service : CartService = Depends(get_cart_service)
):
    try:
        return cart_service.remove_item(customer_id , cart_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=str(e))


@router.delete("/clear_cart" , status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(
        customer_id : UUID,
        cart_service : CartService = Depends(get_cart_service)
):
    try:
        return cart_service.clear_cart(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))



