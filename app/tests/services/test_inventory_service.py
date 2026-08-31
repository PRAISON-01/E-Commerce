from unittest.mock import MagicMock
import pytest
from uuid import uuid4

from _pytest import raises

from app.models.product import Product
from app.models.cart import CartItem
from app.repositories.product_repository import ProductRepository
from app.services.inventory_service import InventoryService
from app.models.store_keeper import StoreKeeper
from app.repositories.storekeeper_repository import StoreKeeperRepository
from models import store_keeper


class TestInventoryService:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock(spec=ProductRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return InventoryService(repository=mock_repo)

    def register_store_keeper(self):
        repo = StoreKeeperRepository(session=Session)
        store_keeper = StoreKeeper()

    def test_increase_stock(self, service, mock_repo):
        product_id = uuid4()
        test_product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )

        mock_repo.find_by_id.return_value = test_product
        mock_repo.save.return_value = test_product

        updated_product = service.add_product(id=product_id, quantity_to_add=10)

        assert updated_product.quantity == 13
        mock_repo.find_by_id.assert_called_once_with(product_id)
        mock_repo.save.assert_called_once_with(test_product)

    def test_decrease_product_quantity(self, service, mock_repo):
        product_id = uuid4()
        test_product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=13
        )
        mock_repo.find_by_id.return_value = test_product
        mock_repo.save.return_value = test_product

        updated_product = service.dispense(id=product_id, quantity_to_remove=10)

        assert updated_product.quantity == 3
        mock_repo.find_by_id.assert_called_once_with(product_id)
        mock_repo.save.assert_called_once_with(test_product)

    @pytest.mark.parametrize("quantity", [
        0,
        -10
    ])
    def test_invalid_quantity_for_add_product(self, quantity, service, mock_repo):
        product_id = uuid4()
        test_product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )

        mock_repo.find_by_id.return_value = test_product
        mock_repo.save.return_value = test_product

        with pytest.raises(ValueError):
            service.add_product(id=product_id, quantity_to_add=quantity)

    @pytest.mark.parametrize("quantity", [
        0,
        -10
    ])
    def test_invalid_quantity_for_dispense(self, quantity, service, mock_repo):
        product_id = uuid4()
        test_product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )

        mock_repo.find_by_id.return_value = test_product
        mock_repo.save.return_value = test_product

        with pytest.raises(ValueError):
            service.dispense(id=product_id, quantity_to_remove=quantity)


    def test_empty_product_stock_dispense_product(self, service, mock_repo):
        product_id = uuid4()
        test_product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )



        mock_repo.find_by_id.return_value = test_product
        mock_repo.save.return_value = test_product

        test_product = service.dispense(id=product_id, quantity_to_remove=3)

        test_product = mock_repo.save(test_product)

        with pytest.raises(ValueError):
            service.dispense(id=product_id, quantity_to_remove=10)


    def test_that_delete_product_deletes_product(self, service, mock_repo):
        product_id = uuid4()
        test_product = Product(
            id=product_id,
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )

        mock_repo.find_by_id.return_value = test_product

        mock_repo.delete_product.return_value = "test_name"

        deleted_product_name = service.delete(id=product_id)

        mock_repo.delete_product.assert_called_once_with(product_id)

        assert deleted_product_name == "test_name"

    def test_that_add_product_require_store_keeper_logged(self, service , mock_repo):
        self.register_store_keeper()
        with pytest.raises(ValueError):
            product_id = uuid4()
            test_product = Product(
                id=product_id,
                name="test_name",
                description="test_description",
                price=5.99,
                quantity=3
            )

            mock_repo.find_by_id.return_value = test_product
            mock_repo.save.return_value = test_product

            service.add_product(id=product_id, quantity_to_add=10)





