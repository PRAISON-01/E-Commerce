import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.exception import AuthenticationException
from app.enums.user_role import UserRole
from app.models.user import User, RegisterUser, LoginUser, LogoutUser
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False})

class TestAuthService:
    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def auth_service(self, session):
        user_repository = UserRepository(session)
        return AuthService(user_repository)

    def test_create_customer(self, session, auth_service):
        payload = RegisterUser(name="John", email="john@gmail.com", password="test-password")
        response = auth_service.create_customer(payload)

        assert response.id is not None
        assert response.name == "John"
        assert response.email == "john@gmail.com"
        assert response.role == UserRole.CUSTOMER

        user = session.get(User, response.id)

        assert user is not None
        assert user.name == "John"
        assert user.email == "john@gmail.com"
        assert user.password == "test-password"
        assert user.role == UserRole.CUSTOMER

    def test_create_customer_raises_exception_when_email_exists(self,session,auth_service):
        user = User(name="John", email="john@gmail.com", password="test-password", role=UserRole.CUSTOMER)
        session.add(user)
        session.commit()

        payload = RegisterUser(name="Another John", email="john@gmail.com", password="another-password")

        with pytest.raises(AuthenticationException,match="Customer with this email already exists"):
            auth_service.create_customer(payload)

    def test_login_customer(self, auth_service):
        auth_service.create_customer(
            RegisterUser(name="John", email="john@gmail.com", password="test-password")
        )
        payload = LoginUser(email="john@gmail.com", password="test-password")
        response = auth_service.login_customer(payload)
        assert response.id is not None
        assert response.name == "John"
        assert response.email == "john@gmail.com"
        assert response.role == UserRole.CUSTOMER
        assert response.is_logged_in is True

    def test_login_customer_raises_exception_when_email_does_not_exist(self, auth_service):
        payload = LoginUser(email="fake@gmail.com", password="test-password")
        with pytest.raises(AuthenticationException, match="Invalid email or password"):
            auth_service.login_customer(payload)

    def test_logout_customer(self, session, auth_service):
        auth_service.create_customer(
            RegisterUser(name="John", email="john@gmail.com", password="test-password")
        )
        auth_service.login_customer(
            LoginUser(email="john@gmail.com",password="test-password")
        )
        payload = LogoutUser(email="john@gmail.com")
        response = auth_service.logout_customer(payload)
        assert response.role == UserRole.CUSTOMER
        assert response.is_logged_in is False
        found_user = session.get(User, response.id)
        assert found_user is not None
        assert found_user.is_logged_in is False

    def test_create_storekeeper(self, session, auth_service):
        payload = RegisterUser( name="Mike", email="mike@gmail.com", password="test-password")
        response = auth_service.create_storekeeper(payload)

        assert response.id is not None
        assert response.name == "Mike"
        assert response.email == "mike@gmail.com"
        assert response.role == UserRole.STOREKEEPER

        user = session.get(User, response.id)

        assert user is not None
        assert user.name == "Mike"
        assert user.email == "mike@gmail.com"
        assert user.password == "test-password"
        assert user.role == UserRole.STOREKEEPER

    def test_create_storekeeper_raises_exception_when_email_exists(self, session, auth_service):
        user = User(name="John", email="john@gmail.com", password="test-password", role=UserRole.STOREKEEPER)
        session.add(user)
        session.commit()

        payload = RegisterUser(name="Another John", email="john@gmail.com", password="another-password")
        with pytest.raises(AuthenticationException,match="StoreKeeper with this email already exists"):
            auth_service.create_storekeeper(payload)



    def test_login_storekeeper(self, auth_service):
        auth_service.create_storekeeper(
            RegisterUser(name="Mike", email="mike@gmail.com", password="test-password")
        )
        payload = LoginUser(email="mike@gmail.com",password="test-password")
        response = auth_service.login_storekeeper(payload)

        assert response.id is not None
        assert response.name == "Mike"
        assert response.email == "mike@gmail.com"
        assert response.role == UserRole.STOREKEEPER
        assert response.is_logged_in is True

    def test_login_storekeeper_raises_exception_when_email_does_not_exist(self, auth_service):
        payload = LoginUser(email="fake@gmail.com", password="test-password")
        with pytest.raises(AuthenticationException, match="Invalid email or password"):
            auth_service.login_storekeeper(payload)

    def test_logout_storekeeper(self, session, auth_service):
        auth_service.create_storekeeper(
            RegisterUser(name="Mike", email="mike@gmail.com", password="test-password")
        )
        auth_service.login_storekeeper(
            LoginUser(email="mike@gmail.com", password="test-password")
        )
        payload = LogoutUser(email="mike@gmail.com")
        response = auth_service.logout_storekeeper(payload)

        assert response.role == UserRole.STOREKEEPER
        assert response.is_logged_in is False
        found_user = session.get(User, response.id)
        assert found_user is not None
        assert found_user.is_logged_in is False
