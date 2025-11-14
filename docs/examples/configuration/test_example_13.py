from dataclasses import dataclass
from typing import Any, Dict

from polyfactory.factories import DataclassFactory


@dataclass
class Product:
    """Product model."""

    name: str
    price: float
    tax_rate: float
    total_price: float


class ProductFactory(DataclassFactory[Product]):
    """Factory for Product with post_generate hook."""

    @classmethod
    def post_generate(cls, result: Dict[str, Any]) -> Dict[str, Any]:
        """Post-generate hook to modify kwargs before model creation.

        This hook is called after field values are generated but before
        the model instance is created, allowing you to compute derived
        fields based on other generated values.
        """
        # Calculate total_price based on price and tax_rate
        price = result["price"]
        tax_rate = result["tax_rate"]
        result["total_price"] = price * (1 + tax_rate)

        return result


def test_post_generate_hook() -> None:
    product = ProductFactory.build()

    # Verify total_price was calculated correctly
    expected_total = product.price * (1 + product.tax_rate)
    assert abs(product.total_price - expected_total) < 0.01

    # Verify with specific values
    product = ProductFactory.build(price=100.0, tax_rate=0.2)
    assert product.total_price == 120.0
