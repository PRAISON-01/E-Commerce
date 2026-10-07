import pytest
from sqlmodel import SQLModel, create_engine, Session

from app.enums.user_role import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository


test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

class TestUserRepository:
    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def saved_user(self, session) -> User:
        user = User(name="John", email="john@gmail.com", password="test-password", role=UserRole.CUSTOMER)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def test_save(self, session):
        repo = UserRepository(session)
        user = User(name="John", email="john@gmail.com", password="test-password", role=UserRole.CUSTOMER)
        saved_user = repo.save(user)

        assert saved_user.id is not None
        assert saved_user.name == "John"
        assert saved_user.email == "john@gmail.com"
        assert saved_user.role == UserRole.CUSTOMER

    def test_find_by_id(self, session, saved_user):
        repo = UserRepository(session)
        found_user = repo.find_by_id(saved_user.id)

        assert found_user is not None
        assert found_user.name == "John"
        assert found_user.email == "john@gmail.com"
        assert found_user.role == UserRole.CUSTOMER

    def test_find_by_email(self, session, saved_user):
        repo = UserRepository(session)
        found_user = repo.find_by_email(saved_user.email)

        assert found_user is not None
        assert found_user.name == "John"
        assert found_user.email == "john@gmail.com"
        assert found_user.role == UserRole.CUSTOMER

    def test_exists_by_email(self, session, saved_user):
        repo = UserRepository(session)
        assert repo.exists_by_email(saved_user.email)