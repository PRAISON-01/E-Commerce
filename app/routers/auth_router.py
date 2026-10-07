from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.config.dependencies import get_session
from app.exception import AuthenticationException
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.models.user import RegisterUser, LoginUser, LogoutUser, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    user_repository = UserRepository(session)
    return AuthService(user_repository)

@router.post("/customers/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_customer(payload: RegisterUser, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.create_customer(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/customers/login", response_model=UserResponse)
def login_customer(payload: LoginUser, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.login_customer(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/customers/logout", response_model=UserResponse)
def logout_customer(payload: LogoutUser, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.logout_customer(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/storekeepers/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_storekeeper(payload: RegisterUser, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.create_storekeeper(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/storekeepers/login",response_model=UserResponse)
def login_storekeeper(payload: LoginUser, auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.login_storekeeper(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=str(e))

@router.post("/storekeepers/logout",response_model=UserResponse)
def logout_storekeeper(payload: LogoutUser,auth_service: AuthService = Depends(get_auth_service)):
    try:
        return auth_service.logout_storekeeper(payload)
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))