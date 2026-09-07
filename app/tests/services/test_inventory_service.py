from uuid import uuid4
import pytest
from pydantic import UUID4, ValidationError
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from app.models.product import Product, AddProduct, UpdateProduct
from app.models.store_keeper import StoreKeeper, RegisterStoreKeeper
from app.models.cart import CartItem, Cart
from app.models.customer import Customer

from app.repositories.product_repository import ProductRepository
from app.repositories.storekeeper_repository import StoreKeeperRepository
from app.services.inventory_service import InventoryService
from app.exception import AuthenticationException
from app.exception.product_not_found_exception import ProductNotFoundException
from app.exception.product_stock_exception import ProductStockException
from app.repositories import storekeeper_repository


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
            repository=product_repo,
            user_repository=storekeeper_repo
        )

    def test_add_product_user_not_found(self, service):
        non_existent_user_email = "testemail@gmail.com"
        payload = AddProduct(
            name="Test Item",
            description="test_description",
            price=19.99,
            quantity=10,
            store_keeper_email=non_existent_user_email
        )

        with pytest.raises(AuthenticationException):
            service.add_product(payload)

    def test_dispense_product_user_not_found(self,session,  service):
        id = uuid4()

        product = Product(
            id=id,
            name="Test Product",
            description="Test Description",
            price=5.99,
            quantity=10,
        )

        session.add(product)
        session.commit()

        non_existent_user_email = "testemail@gmail.com"
        with pytest.raises(AuthenticationException):
            service.dispense(
                id=id,
                store_keeper_email=non_existent_user_email,
                quantity_to_remove=3
            )

    def test_delete_product_user_not_found(self, service):
        id = uuid4()
        non_existent_user_email = "testemail@gmail.com"

        with pytest.raises(AuthenticationException):
            service.delete(id, store_keeper_email=non_existent_user_email)

    def test_get_product_user_not_found(self, service):
        id = uuid4()
        non_existent_user_email = "testemail@gmail.com"

        with pytest.raises(AuthenticationException):
            service.get_product(id, store_keeper_email=non_existent_user_email)

    def test_get_all_product_user_not_found(self, service):
        non_existent_user_email = "testemail@gmail.com"

        with pytest.raises(AuthenticationException):
            service.get_all_products(store_keeper_email=non_existent_user_email)

    def test_add_product_store_keeper_not_logged_in(self, session, service):
        store_keeper_email = "testemail@gmail.com"
        id = uuid4()
        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=False
        )
        session.add(user)
        session.commit()

        payload = AddProduct(
            name="Test Item",
            description="test_description",
            price=19.99,
            quantity=10,
            store_keeper_email=store_keeper_email
        )

        with pytest.raises(AuthenticationException):
            service.add_product(payload)

    def test_cannot_dispense_when_store_keeper_not_logged_in(
            self,
            session,
            service,
    ):
        store_keeper_email = "test@gmail.com"
        id = uuid4()

        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=False,
        )

        product = Product(
            id=id,
            name="Test Product",
            description="Test Description",
            price=5.99,
            quantity=10,
        )

        session.add(user)
        session.add(product)
        session.commit()

        with pytest.raises(AuthenticationException):
            service.dispense(
                id=id,
                store_keeper_email=store_keeper_email,
                quantity_to_remove=3,
            )

    def test_cannot_delete_when_store_keeper_not_logged_in(
            self,
            session,
            service,
    ):
        store_keeper_email = "testemail@gmail.com"
        id = uuid4()

        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=False,
        )

        product = Product(
            id=id,
            name="Test Product",
            description="Test Description",
            price=5.99,
            quantity=10,
        )

        session.add(user)
        session.add(product)
        session.commit()

        with pytest.raises(AuthenticationException):
            service.delete(
                id=id,
                store_keeper_email=store_keeper_email,
            )


    def test_cannot_get_product_when_store_keeper_not_logged_in(
            self,
            session,
            service,
    ):
        store_keeper_email = "testemail@gmail.com"
        id = uuid4()

        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=False,
        )

        product = Product(
            id=id,
            name="Test Product",
            description="Test Description",
            price=5.99,
            quantity=10,
        )

        session.add(user)
        session.add(product)
        session.commit()

        with pytest.raises(AuthenticationException):
            service.get_product(
                id=id,
                store_keeper_email=store_keeper_email,
            )

    def test_cannot_get_all_products_when_store_keeper_not_logged_in(
            self,
            session,
            service,
    ):
        store_keeper_email = "testemail@gmail.com"
        id = uuid4()

        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=False,
        )

        product = Product(
            id=id,
            name="Test Product",
            description="Test Description",
            price=5.99,
            quantity=10,
        )

        session.add(user)
        session.add(product)
        session.commit()

        with pytest.raises(AuthenticationException):
            service.get_all_products(
                store_keeper_email=store_keeper_email,
            )

    def test_increase_stock(self, session, service, product_repo, storekeeper_repo):
        store_keeper_email = "testemail@gmail.com"


        user = StoreKeeper(
            id=uuid4(),
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=True
        )
        sk = storekeeper_repo.save(user)

        initial_product = Product(
            name="testing",
            description="test_description",
            price=19.99,
            quantity=10,
        )
        saved_product = product_repo.save(initial_product)

        updated_payload = UpdateProduct(
            id=saved_product.id,
            name="test_name",
            description="test_description",
            price=19.99,
            quantity=10,
            store_keeper_email=sk.email
        )

        updated_product = service.restock(updated_payload)

        assert updated_product.quantity == 20

        session.expire_all()
        session.refresh(saved_product)
        assert saved_product.quantity == 20

    @pytest.mark.parametrize("quantity", [0, -10])
    def test_invalid_quantity_for_add_product(self, quantity, session, service):
        store_keeper_email = "testemail@gmail.com"
        id = uuid4()

        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test_email@gmail.com",
            password="test_password",
            is_logged_in=True
        )
        session.add(user)
        session.commit()



        with pytest.raises(ValidationError):
            AddProduct(
                name="Test Item",
                description="test_description",
                price=19.99,
                quantity=quantity,
                store_keeper_email=store_keeper_email
            )


    def test_decrease_product_quantity(self, session, service, product_repo, storekeeper_repo):
        store_keeper_email = "testemail@gmail.com"
        id = uuid4()

        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test@gmail.com",
            password="test_password",
            is_logged_in=True
        )
        sk = storekeeper_repo.save(user)

        initial_product = Product(
            name="testing",
            description="test_description",
            price=19.99,
            quantity=10,
        )
        saved_product = product_repo.save(initial_product)

        saved_product = service.dispense(saved_product.id, store_keeper_email=sk.email, quantity_to_remove=10)

        assert saved_product.quantity == 0




    @pytest.mark.parametrize("quantity", [0, -10])
    def test_invalid_quantity_for_dispense_more_than_available_product(self,session,  quantity, service, product_repo):

        user = StoreKeeper(
            id=uuid4(),
            name="test_storekeeper",
            email="test_email@gmail.com",
            password="test_password",
            is_logged_in=True
        )

        session.add(user)
        session.commit()

        payload = Product(
            name="Test Item",
            description="test_description",
            price=19.99,
            quantity=10,
        )

        saved = product_repo.save(payload)



        with pytest.raises(ProductStockException):
            service.dispense(saved.id, store_keeper_email=user.email, quantity_to_remove=quantity)

    def test_empty_product_stock_dispense_product(self, session, service):
        store_keeper_email = "testemail@gmail.com"


        user = StoreKeeper(
            id=uuid4(),
            name="test_storekeeper",
            email=store_keeper_email,
            password="test_password",
            is_logged_in=True
        )

        id = uuid4()
        product = Product(
            id=id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        session.add(user)
        session.add(product)
        session.commit()

        with pytest.raises(ProductStockException):
            service.dispense(id=id, store_keeper_email=store_keeper_email, quantity_to_remove=10)

    def test_that_delete_product_deletes_product(self, session, service, product_repo):

        user = StoreKeeper(
            id = uuid4(),
            name="test_name",
            email="test@gmail.com",
            password="12345678",
            is_logged_in=True
        )

        sk_repo = StoreKeeperRepository(session)

        saved_store_keeper = sk_repo.save(user)

        product = Product(
            id=uuid4(),
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        saved = product_repo.save(product)
        service.delete(id=saved.id, store_keeper_email=user.email)

        product_repo.find_by_id(saved.id) is None

    def test_that_get_product_with_invalid_id_raise_valueError(self, session, service):
        store_keeper_email = uuid4()

        user = StoreKeeper(
            id=uuid4(),
            name="test_storekeeper",
            email="test_email@gmail.com",
            password="test_password",
            is_logged_in=True
        )

        session.add(user)
        session.commit()

        id = uuid4()

        with pytest.raises(ProductNotFoundException):
            service.get_product(id, user.email)

    def test_that_get_product_with_valid_id(self, session, service, product_repo):
        store_keeper_email = uuid4()
        id = uuid4()


        user = StoreKeeper(
            id=id,
            name="test_storekeeper",
            email="test_email@gmail.com",
            password="test_password",
            is_logged_in=True
        )

        session.add(user)
        session.commit()

        id = uuid4()
        product = Product(
            id=id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )
        session.add(product)
        session.commit()

        product_repo.save(product)

        found_product = service.get_product(id=id, store_keeper_email=user.email)
        assert found_product.name == "test_name"
        assert session.get(Product, id).id == found_product.id
