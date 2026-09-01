from uuid import uuid4
import pytest
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from app.models.product import Product
from app.models.store_keeper import StoreKeeper
from app.models.cart import CartItem, Cart
from app.models.customer import Customer

from app.repositories.product_repository import ProductRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.services.inventory_service import InventoryService

class TestInventoryServiceIntegration:
    @pytest.fixture(name="session")
    def session_fixture(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            yield session
        SQLModel.metadata.drop_all(engine)

    @pytest.fixture
    def product_repo(self, session):
        return ProductRepository(session=session)

    @pytest.fixture
    def storekeeper_repo(self, session):
        return StoreKeeperRepository(session=session)

    @pytest.fixture
    def service(self, session, product_repo, storekeeper_repo):
        return InventoryService(
            session=session,
            repository=product_repo,
            user_repository=storekeeper_repo
        )

    def test_increase_stock(self, session, service):
        store_keeper_id = uuid4()
        user = StoreKeeper(
            id=store_keeper_id,
            name="Keeper",
            email="keeper@test.com",
            password="hashed_password",
            is_logged_in=True
        )

        product_id = uuid4()
        product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        session.add(user)
        session.add(product)
        session.commit()

        updated_product = service.add_product(
            id=product_id,
            store_keeper_id=store_keeper_id,
            quantity_to_add=10
        )

        assert updated_product.quantity == 13

        session.refresh(product)
        assert product.quantity == 13

    def test_add_product_user_not_found(self, service):
        product_id = uuid4()
        non_existent_user_id = uuid4()

        result = service.add_product(
            id=product_id,
            store_keeper_id=non_existent_user_id,
            quantity_to_add=10
        )

        assert result == "User not found!"

    def test_add_product_store_keeper_not_logged_in(self, session, service):
        store_keeper_id = uuid4()
        user = StoreKeeper(
            id=store_keeper_id,
            name="Keeper",
            email="test@gmail.com",
            password="hashed_password",
            is_logged_in=False  # Not logged in
        )
        session.add(user)
        session.commit()

        result = service.add_product(
            id=uuid4(),
            store_keeper_id=store_keeper_id,
            quantity_to_add=10
        )

        assert result == " test@gmail.com not logged in!"

    @pytest.mark.parametrize("quantity", [0, -10])
    def test_invalid_quantity_for_add_product(self, quantity, session, service):
        store_keeper_id = uuid4()
        user = StoreKeeper(
            id=store_keeper_id,
            name="Keeper",
            email="keeper@test.com",
            password="hashed_password",
            is_logged_in=True
        )
        session.add(user)
        session.commit()

        with pytest.raises(ValueError, match="Invalid Amount!!!"):
            service.add_product(
                id=uuid4(),
                store_keeper_id=store_keeper_id,
                quantity_to_add=quantity
            )

    def test_decrease_product_quantity(self, session, service):
        product_id = uuid4()
        product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=13
        )
        session.add(product)
        session.commit()

        updated_product = service.dispense(id=product_id, quantity_to_remove=10)

        assert updated_product.quantity == 3
        session.refresh(product)
        assert product.quantity == 3

    @pytest.mark.parametrize("quantity", [0, -10])
    def test_invalid_quantity_for_dispense(self, quantity, service):
        with pytest.raises(ValueError, match="Invalid Amount!!!"):
            service.dispense(id=uuid4(), quantity_to_remove=quantity)

    def test_empty_product_stock_dispense_product(self, session, service):
        product_id = uuid4()
        product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        session.add(product)
        session.commit()

        service.dispense(id=product_id, quantity_to_remove=3)

        with pytest.raises(ValueError, match="Not enough stock available!!!"):
            service.dispense(id=product_id, quantity_to_remove=10)

    def test_that_delete_product_deletes_product(self, session, service):
        product_id = uuid4()
        product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        session.add(product)
        session.commit()

        deleted_product_name = service.delete(id=product_id)
        assert deleted_product_name == "test_name"
        assert session.get(Product, product_id) is None


    def test_that_get_product_with_invalid_product_id_raise_valueError(self, session, service):
        product_id = uuid4()

        with pytest.raises(ValueError):
            service.get_product(product_id)

    def test_that_get_product_with_valid_product_id(self, session, service, product_repo):
        product_id = uuid4()
        product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        session.add(product)
        session.commit()

        product_repo.save(product)



        found_product = service.get_product(id=product_id)
        assert found_product.name == "test_name"
        assert session.get(Product, product_id).id == found_product.id