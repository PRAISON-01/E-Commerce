from app.exception import AuthenticationException
from app.repositories.user_repository import UserRepository
from app.models.user import User, RegisterUser, LoginUser, LogoutUser, UserResponse
from app.enums.user_role import UserRole


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_customer(self, payload: RegisterUser) -> UserResponse:
        if self.user_repository.exists_by_email(payload.email):
            raise AuthenticationException(
                "Customer with this email already exists"
            )

        data = payload.model_dump()

        user = User(
            **data,
            role=UserRole.CUSTOMER
        )

        user = self.user_repository.save(user)

        return UserResponse.model_validate(user)

    def login_customer(self, payload: LoginUser) -> UserResponse:
        found_user = self.user_repository.find_by_email(payload.email)

        if found_user is None:
            raise AuthenticationException("Invalid email or password")

        if found_user.role != UserRole.CUSTOMER:
            raise AuthenticationException("Invalid email or password")

        if payload.password != found_user.password:
            raise AuthenticationException("Invalid email or password")

        found_user.is_logged_in = True

        found_user = self.user_repository.save(found_user)

        return UserResponse.model_validate(found_user)

    def logout_customer(self, payload: LogoutUser) -> UserResponse:
        found_user = self.user_repository.find_by_email(payload.email)

        if found_user is None:
            raise AuthenticationException("Customer not found")

        if found_user.role != UserRole.CUSTOMER:
            raise AuthenticationException("Customer not found")

        found_user.is_logged_in = False

        found_user = self.user_repository.save(found_user)

        return UserResponse.model_validate(found_user)

    def create_storekeeper(self, payload: RegisterUser) -> UserResponse:
        if self.user_repository.exists_by_email(payload.email):
            raise AuthenticationException(
                "StoreKeeper with this email already exists"
            )

        data = payload.model_dump()

        user = User(
            **data,
            role=UserRole.STOREKEEPER
        )

        user = self.user_repository.save(user)

        return UserResponse.model_validate(user)

    def login_storekeeper(self, payload: LoginUser) -> UserResponse:
        found_user = self.user_repository.find_by_email(payload.email)

        if found_user is None:
            raise AuthenticationException("Invalid email or password")

        if found_user.role != UserRole.STOREKEEPER:
            raise AuthenticationException("Invalid email or password")

        if payload.password != found_user.password:
            raise AuthenticationException("Invalid email or password")

        found_user.is_logged_in = True

        found_user = self.user_repository.save(found_user)

        return UserResponse.model_validate(found_user)

    def logout_storekeeper(self, payload: LogoutUser) -> UserResponse:
        found_user = self.user_repository.find_by_email(payload.email)

        if found_user is None:
            raise AuthenticationException("StoreKeeper not found")

        if found_user.role != UserRole.STOREKEEPER:
            raise AuthenticationException("StoreKeeper not found")

        found_user.is_logged_in = False

        found_user = self.user_repository.save(found_user)

        return UserResponse.model_validate(found_user)