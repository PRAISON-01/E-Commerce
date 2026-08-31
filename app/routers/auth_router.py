from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.config.dependencies import get_session
from app.exception import AuthenticationException
from app.repositories.customer_repository import CustomerRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.services.auth_service import AuthService
from app.models.customer import RegisterCustomer, LoginCustomer, CustomerResponse, LogoutCustomer
from app.models.store_keeper import RegisterStoreKeeper, LoginStoreKeeper, StoreKeeperResponse, LogoutStoreKeeper

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    customer_repository = CustomerRepository(session)
    storekeeper_repository = StoreKeeperRepository(session)
    return AuthService(customer_repository, storekeeper_repository)


@router.post("/customers/register", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def register_customer(payload: RegisterCustomer, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.create_customer(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/customers/login", response_model=CustomerResponse)
def login_customer(payload: LoginCustomer, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.login_customer(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/customers/logout", response_model=CustomerResponse)
def logout_customer(payload: LogoutCustomer, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.logout_customer(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/storekeepers/register", response_model=StoreKeeperResponse, status_code=status.HTTP_201_CREATED)
def register_storekeeper(payload: RegisterStoreKeeper, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.create_storekeeper(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/storekeepers/login", response_model=StoreKeeperResponse)
def login_storekeeper(payload: LoginStoreKeeper, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.login_storekeeper(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/storekeepers/logout", response_model=StoreKeeperResponse)
def logout_storekeeper(payload: LogoutStoreKeeper, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.logout_storekeeper(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))