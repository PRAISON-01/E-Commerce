from uuid import uuid4

import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False}
)

class TestCustomerRepository:

    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def saved_customer(self, session) -> Customer:
        customer = Customer(name="John", email="john@gmail.com", password="test-password")
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    def test_save(self, session):
        repo = CustomerRepository(session)
        customer = Customer(name="John", email="john@gmail.com", password="test-password")
        saved_customer = repo.save(customer)

        assert saved_customer.id is not None
        assert saved_customer.name == "John"
        assert saved_customer.email == "john@gmail.com"

    def test_save_then_update_existing_customer(self, session, saved_customer):
        repo = CustomerRepository(session)
        saved_customer.name = "Johnny"
        updated_customer = repo.save(saved_customer)

        assert updated_customer.name == "Johnny"
        assert updated_customer.id == saved_customer.id
        found_customer = repo.find_by_id(saved_customer.id)
        assert found_customer.name == "Johnny"

    def test_find_by_id(self, session, saved_customer):
        repo = CustomerRepository(session)
        found_customer = repo.find_by_id(saved_customer.id)
        assert found_customer is not None
        assert found_customer.name == "John"
        assert found_customer.email == "john@gmail.com"

    def test_find_by_id_returns_none_when_customer_does_not_exist(
        self,session):
        repo = CustomerRepository(session)
        found_customer = repo.find_by_id(uuid4())
        assert found_customer is None

    def test_find_by_email(self, session, saved_customer):
        repo = CustomerRepository(session)
        found_customer = repo.find_by_email(saved_customer.email)
        assert found_customer is not None
        assert found_customer.name == "John"
        assert found_customer.email == "john@gmail.com"

    def test_find_by_email_returns_none_when_customer_does_not_exist(
        self,session):
        repo = CustomerRepository(session)
        found_customer = repo.find_by_email("fake@gmail.com")
        assert found_customer is None

    def test_exists_by_email(self, session, saved_customer):
        repo = CustomerRepository(session)
        assert repo.exists_by_email(saved_customer.email)

    def test_exists_by_email_returns_false_when_customer_does_not_exist(
        self,session):
        repo = CustomerRepository(session)
        assert not repo.exists_by_email("fake@gmail.com")