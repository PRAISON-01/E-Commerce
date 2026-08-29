import pytest
from sqlalchemy import StaticPool, create_engine
from sqlmodel import SQLModel, Session

from models.product import AddProduct
from repositories.product_repository import ProductRepository
class TestProductRepository:
    @pytest.fixture
    def db_session(self):
        test_engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(test_engine)

        with Session(test_engine) as session:
            yield session

        SQLModel.metadata.drop_all(test_engine)


    def create_test_product(self):
        product = AddProduct(
            name = "test_name",
            description = "test_description",
            price = 5.99,
            quantity = 3
        )

        return product

    def test_that_save_product_saved_product_id_is_created(self, db_session : Session):

        repo = ProductRepository(session = db_session)

        product = self.create_test_product()

        saved_product = repo.save(product)

        assert saved_product.id is not None


    def test_that_save_product_saved_product_find_by_id_returns_product(self, db_session : Session):

        repo = ProductRepository(session = db_session)

        product = self.create_test_product()

        saved_product = repo.save(product)

        assert saved_product.id is not None


        print(f"There you are >> {saved_product.id}")
        assert repo.find_by_id(saved_product.id) == saved_product


