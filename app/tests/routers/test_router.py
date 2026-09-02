import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.main import app
from config.dependencies import get_session
from app.models.customer import Customer
from app.models.store_keeper import StoreKeeper
from sqlalchemy.pool import StaticPool

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

class TestAuthRouter:
    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(test_engine)
        with Session(test_engine) as session:
            yield session
        SQLModel.metadata.drop_all(test_engine)

    @pytest.fixture
    def client(self, session):
        def override_get_session():
            yield session

        app.dependency_overrides[get_session] = override_get_session
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()

    def test_register_customer(self, client):
        payload = {"name": "John", "email": "john@gmail.com", "password": "test-password"}
        response = client.post("/auth/customers/register", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["id"] is not None
        assert body["name"] == "John"
        assert body["email"] == "john@gmail.com"
        assert "password" not in body

    def test_register_customer_fails_when_email_exists(self, session, client):
        session.add(Customer(name="John", email="john@gmail.com", password="test-password"))
        session.commit()

        payload = {"name": "Another John", "email": "john@gmail.com", "password": "another-password"}
        response = client.post("/auth/customers/register", json=payload)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_login_customer(self, client):
        client.post("/auth/customers/register", json={
            "name": "John", "email": "john@gmail.com", "password": "test-password"})

        response = client.post("/auth/customers/login", json={
            "email": "john@gmail.com", "password": "test-password"})
        assert response.status_code == 200
        body = response.json()
        assert body["email"] == "john@gmail.com"

    def test_login_customer_fails_when_email_does_not_exist(self, client):
        response = client.post("/auth/customers/login", json={
            "email": "fake@gmail.com", "password": "test-password"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

    def test_login_customer_fails_when_password_is_wrong(self, client):
        client.post("/auth/customers/register", json={
            "name": "John", "email": "john@gmail.com", "password": "test-password"})

        response = client.post("/auth/customers/login", json={
            "email": "john@gmail.com", "password": "wrong-password"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

    def test_register_storekeeper(self, client):
        payload = {"name": "Mike", "email": "mike@gmail.com", "password": "test-password"}
        response = client.post("/auth/storekeepers/register", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Mike"
        assert body["email"] == "mike@gmail.com"

    def test_register_storekeeper_fails_when_email_exists(self, session, client):
        session.add(StoreKeeper(name="Mike", email="mike@gmail.com", password="test-password"))
        session.commit()

        payload = {"name": "Another Mike", "email": "mike@gmail.com", "password": "another-password"}
        response = client.post("/auth/storekeepers/register", json=payload)
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_login_storekeeper(self, client):
        client.post("/auth/storekeepers/register", json={
            "name": "Mike", "email": "mike@gmail.com", "password": "test-password"})

        response = client.post("/auth/storekeepers/login", json={
            "email": "mike@gmail.com", "password": "test-password"})
        assert response.status_code == 200
        assert response.json()["email"] == "mike@gmail.com"

    def test_login_storekeeper_fails_when_password_is_wrong(self, client):
        client.post("/auth/storekeepers/register", json={
            "name": "Mike", "email": "mike@gmail.com", "password": "test-password"})

        response = client.post("/auth/storekeepers/login", json={
            "email": "mike@gmail.com", "password": "wrong-password"})
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"