import pytest
from pydantic import ValidationError

from app.models.product import AddProduct, UpdateProduct


class TestProductModel:

    @pytest.mark.parametrize("name", [
        " ",
        "na",
    ])
    def test_product_with_invalid_name_(self, name):
        with pytest.raises(ValidationError):
            AddProduct(
                name=name,
                description="Crunchy",
                price=5.99,
                quantity=3,
            )

    @pytest.mark.parametrize("description", [
        " ",
        "de",
    ])
    def test_product_with_invalid_description_(self, description):
        with pytest.raises(ValidationError):
            AddProduct(
                name="test_name",
                description=description,
                price=5.99,
                quantity=3,
            )

    @pytest.mark.parametrize("price", [
        0,
        -1
        -1000
    ])
    def test_product_with_invalid_price_(self, price):
        with pytest.raises(ValidationError):
            AddProduct(
                name ="test_name",
                description="test_description",
                price=price,
                quantity=3,
            )


    @pytest.mark.parametrize("quantity", [
        0,
        -1,
        -1000
    ])

    def test_product_with_invalid_quantity(self, quantity):
        with pytest.raises(ValidationError):
            AddProduct(
                name = "test_name",
                description="test_description",
                price=5.99,
                quantity=quantity,
            )


# Valid Parameters

    def test_product_with_valid_name_(self):
        product = AddProduct(
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3,
        )

        assert product.name == "test_name"
        assert product.description == "test_description"
        assert product.price == 5.99
        assert product.quantity == 3


@pytest.fixture
def start_all_block_with_this():
    product = AddProduct(
        name="test_name",
        description="test_description",
        price=5.99,
        quantity=3,
    )

    return product


class TestUpdateProduct:

    @pytest.mark.parametrize("name", [
        " ",
        "de",
    ])
    def test_product_with_invalid_name_(self, name):

        with pytest.raises(ValueError):
            UpdateProduct(
                name = name,
                description="test_description",
                price=5.99,
                quantity=3
            )

    @pytest.mark.parametrize("description", [
        " ",
        "de",
    ])
    def test_product_with_invalid_description_(self, description):

        with pytest.raises(ValueError):
            UpdateProduct(
                name = "test_name",
                description=description,
                price=5.99,
                quantity=3
            )


    @pytest.mark.parametrize("price", [
        0,
        -1000,
        -10000000000
    ])
    def test_product_with_invalid_price(self, price):

        with pytest.raises(ValueError):
            UpdateProduct(
                name = "test_name",
                description="test_description",
                price=price,
                quantity=3
            )

    @pytest.mark.parametrize("quantity", [
        0,
        -1000,
        -10000000000
    ])
    def test_product_with_invalid_quantity(self, quantity):

        with pytest.raises(ValueError):
            UpdateProduct(
                name = "test_name",
                description="test_description",
                price=5.99,
                quantity=quantity
            )

    def test_update_product_with_valid_parameters(self):
        product = UpdateProduct(
            name="test_name",
            description="test_description",
            price=5.99,
            quantity=3
        )

        assert product.name == "test_name"
        assert product.description == "test_description"
        assert product.price == 5.99
        assert product.quantity == 3