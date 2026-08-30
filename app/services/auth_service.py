from app.exception import AuthenticationException
from app.repositories.customer_repository import CustomerRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.models.customer import (Customer, RegisterCustomer, LoginCustomer, CustomerResponse, LogoutCustomer)
from app.models.store_keeper import (StoreKeeper, RegisterStoreKeeper, LoginStoreKeeper, StoreKeeperResponse, LogoutStoreKeeper)


class AuthService:
    def __init__(self, customer_repository: CustomerRepository, storekeeper_repository: StoreKeeperRepository):
        self.customer_repository = customer_repository
        self.storekeeper_repository = storekeeper_repository

    def create_customer(self, payload: RegisterCustomer) -> CustomerResponse:
        if self.customer_repository.exists_by_email(payload.email):
            raise AuthenticationException("Customer with this email already exists")
        data = payload.model_dump()
        customer = Customer(**data)

        customer = self.customer_repository.save(customer)
        return CustomerResponse.model_validate(customer)

    def login_customer(self, payload: LoginCustomer) -> CustomerResponse:
        found_customer = self.customer_repository.find_by_email(payload.email)
        if found_customer is None:
            raise AuthenticationException("Invalid email or password")

        if payload.password != found_customer.password:
            raise AuthenticationException("Invalid email or password")
        found_customer.is_logged_in = True
        found_customer = self.customer_repository.save(found_customer)
        return CustomerResponse.model_validate(found_customer)

    def logout_customer(self, payload: LogoutCustomer) -> CustomerResponse:
        found_customer = self.customer_repository.find_by_email(payload.email)
        if found_customer is None:
            raise AuthenticationException("Customer not found")
        found_customer.is_logged_in = False
        found_customer = self.customer_repository.save(found_customer)
        return CustomerResponse.model_validate(found_customer)

    def create_storekeeper(self, payload: RegisterStoreKeeper) -> StoreKeeperResponse:
        if self.storekeeper_repository.exists_by_email(payload.email):
            raise AuthenticationException("StoreKeeper with this email already exists")
        data = payload.model_dump()
        storekeeper = StoreKeeper(**data)
        storekeeper = self.storekeeper_repository.save(storekeeper)
        return StoreKeeperResponse.model_validate(storekeeper)

    def login_storekeeper(self, payload: LoginStoreKeeper) -> StoreKeeperResponse:
        found_storekeeper = self.storekeeper_repository.find_by_email(payload.email)
        if found_storekeeper is None:
            raise AuthenticationException("Invalid email or password")
        if payload.password != found_storekeeper.password:
            raise AuthenticationException("Invalid email or password")
        found_storekeeper.is_logged_in = True
        found_storekeeper = self.storekeeper_repository.save(found_storekeeper)
        return StoreKeeperResponse.model_validate(found_storekeeper)

    def logout_storekeeper(self, payload: LogoutStoreKeeper) -> StoreKeeperResponse:
        found_storekeeper = self.storekeeper_repository.find_by_email(payload.email)
        if found_storekeeper is None:
            raise AuthenticationException("StoreKeeper not found")
        found_storekeeper.is_logged_in = False
        found_storekeeper = self.storekeeper_repository.save(found_storekeeper)
        return StoreKeeperResponse.model_validate(found_storekeeper)