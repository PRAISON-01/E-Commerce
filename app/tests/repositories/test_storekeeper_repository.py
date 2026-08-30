from uuid import uuid4

import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.models.store_keeper import StoreKeeper
from app.repositories.storekeeper_repository import StoreKeeperRepository

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

class TestStoreKeeperRepository:

    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def saved_storekeeper(self, session) -> StoreKeeper:
        storekeeper = StoreKeeper(name="John", email="john@gmail.com", password="test-password")
        session.add(storekeeper)
        session.commit()
        session.refresh(storekeeper)
        return storekeeper

    def test_save(self, session):
        repo = StoreKeeperRepository(session)
        storekeeper = StoreKeeper(name="John", email="john@gmail.com", password="test-password")
        saved_storekeeper = repo.save(storekeeper)

        assert saved_storekeeper.id is not None
        assert saved_storekeeper.name == "John"
        assert saved_storekeeper.email == "john@gmail.com"

    def test_save_then_update_existing_customer(self, session, saved_storekeeper):
        repo = StoreKeeperRepository(session)
        saved_storekeeper.name = "Johnny"
        updated_storekeeper = repo.save(saved_storekeeper)

        assert updated_storekeeper.name == "Johnny"
        assert updated_storekeeper.id == saved_storekeeper.id
        found_storekeeper = repo.find_by_id(saved_storekeeper.id)
        assert found_storekeeper.name == "Johnny"

    def test_find_by_id(self, session, saved_storekeeper):
        repo = StoreKeeperRepository(session)
        found_storekeeper = repo.find_by_id(saved_storekeeper.id)

        assert found_storekeeper is not None
        assert found_storekeeper.name == "John"
        assert found_storekeeper.email == "john@gmail.com"

    def test_find_by_id_returns_none_when_storekeeper_does_not_exist(
        self,session):
        repo = StoreKeeperRepository(session)
        found_storekeeper = repo.find_by_id(uuid4())
        assert found_storekeeper is None

    def test_find_by_email(self, session, saved_storekeeper):
        repo = StoreKeeperRepository(session)
        found_storekeeper = repo.find_by_email(saved_storekeeper.email)
        assert found_storekeeper is not None
        assert found_storekeeper.name == "John"
        assert found_storekeeper.email == "john@gmail.com"

    def test_find_by_email_returns_none_when_storekeeper_does_not_exist(
        self,session):
        repo = StoreKeeperRepository(session)
        found_storekeeper = repo.find_by_email("fake@gmail.com")
        assert found_storekeeper is None

    def test_exists_by_email(self, session, saved_storekeeper):
        repo = StoreKeeperRepository(session)
        assert repo.exists_by_email(saved_storekeeper.email)

    def test_exists_by_email_returns_false_when_storekeeper_does_not_exist(
        self,session):
        repo = StoreKeeperRepository(session)
        assert not repo.exists_by_email("fake@gmail.com")

