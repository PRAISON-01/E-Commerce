import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.exception import AuthenticationException
from app.models.customer import (Customer, RegisterCustomer, LoginCustomer)
from app.models.store_keeper import (StoreKeeper, RegisterStoreKeeper, LoginStoreKeeper)
from app.repositories.customer_repository import CustomerRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.services.auth_service import AuthService

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

class TestAuthService:
    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def auth_service(self, session):
        customer_repository = CustomerRepository(session)
        storekeeper_repository = StoreKeeperRepository(session)
        return AuthService(customer_repository, storekeeper_repository)

    def test_create_customer(self, session, auth_service):
        payload = RegisterCustomer(name="John", email="john@gmail.com", password="test-password")
        response = auth_service.create_customer(payload)

        assert response.id is not None
        assert response.name == "John"
        assert response.email == "john@gmail.com"
        customer = session.get(Customer, response.id)

        assert customer is not None
        assert customer.name == "John"
        assert customer.email == "john@gmail.com"
        assert customer.password == "test-password"

    def test_create_customer_raises_exception_when_email_exists(self, session, auth_service):
        customer = Customer(name="John", email="john@gmail.com", password="test-password")
        session.add(customer)
        session.commit()

        payload = RegisterCustomer(name="Another John", email="john@gmail.com", password="another-password")
        with pytest.raises(AuthenticationException, match="Customer with this email already exists"):
            auth_service.create_customer(payload)

    def test_login_customer(self, session, auth_service):
        auth_service.create_customer(RegisterCustomer(name="John", email="john@gmail.com", password="test-password"))

        payload = LoginCustomer(email="john@gmail.com", password="test-password")
        response = auth_service.login_customer(payload)
        assert response.id is not None
        assert response.name == "John"
        assert response.email == "john@gmail.com"

    def test_login_customer_raises_exception_when_email_does_not_exist(self, auth_service):
        payload = LoginCustomer(email="fake@gmail.com", password="test-password")
        with pytest.raises(AuthenticationException, match="Invalid email or password"):
            auth_service.login_customer(payload)

    def test_login_customer_raises_exception_when_password_is_wrong(self, auth_service):
        auth_service.create_customer(
            RegisterCustomer(name="John", email="john@gmail.com", password="test-password")
        )

        payload = LoginCustomer(email="john@gmail.com", password="wrong-password")
        with pytest.raises(AuthenticationException, match="Invalid email or password"):
            auth_service.login_customer(payload)

    def test_create_storekeeper(self, session, auth_service):
        payload = RegisterStoreKeeper(name="Mike", email="mike@gmail.com", password="test-password")
        response = auth_service.create_storekeeper(payload)

        assert response.id is not None
        assert response.name == "Mike"
        assert response.email == "mike@gmail.com"

        storekeeper = session.get(StoreKeeper, response.id)

        assert storekeeper is not None
        assert storekeeper.name == "Mike"
        assert storekeeper.email == "mike@gmail.com"
        assert storekeeper.password == "test-password"

    def test_create_storekeeper_raises_exception_when_email_exists(self, session, auth_service):
        storekeeper = StoreKeeper(name="Mike", email="mike@gmail.com", password="test-password")
        session.add(storekeeper)
        session.commit()

        payload = RegisterStoreKeeper(name="Another Mike", email="mike@gmail.com",password="another-password")
        with pytest.raises(AuthenticationException, match="StoreKeeper with this email already exists"):
            auth_service.create_storekeeper(payload)

    def test_login_storekeeper(self, auth_service):
        auth_service.create_storekeeper(
            RegisterStoreKeeper(name="Mike", email="mike@gmail.com", password="test-password")
        )
        payload = LoginStoreKeeper(email="mike@gmail.com", password="test-password")
        response = auth_service.login_storekeeper(payload)

        assert response.id is not None
        assert response.name == "Mike"
        assert response.email == "mike@gmail.com"

    def test_login_storekeeper_raises_exception_when_email_does_not_exist(self, auth_service):
        payload = LoginStoreKeeper(email="fake@gmail.com", password="test-password")
        with pytest.raises(AuthenticationException, match="Invalid email or password"):
            auth_service.login_storekeeper(payload)

    def test_login_storekeeper_raises_exception_when_password_is_wrong(self, auth_service):
        auth_service.create_storekeeper(
            RegisterStoreKeeper(name="Mike", email="mike@gmail.com", password="test-password")
        )
        payload = LoginStoreKeeper(email="mike@gmail.com", password="wrong-password")
        with pytest.raises(AuthenticationException, match="Invalid email or password"):
            auth_service.login_storekeeper(payload)