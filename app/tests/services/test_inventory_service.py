from unittest.mock import MagicMock
import pytest
from uuid import uuid4

from repositories.product_repository import ProductRepository
from services.inventory_service import InventoryService


class TestInventoryService:
    @pytest.fixture
    def mock_repo(self):
        return MagicMock(spec=ProductRepository)

    @pytest.fixture
    def service(self, mock_repo):
        return InventoryService(repository=mock_repo)

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


