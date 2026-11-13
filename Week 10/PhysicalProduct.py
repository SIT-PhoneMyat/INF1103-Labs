from math import isfinite

from CanBeShipped import CanBeShipped
from Product import Product
from Supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    SHIPPING_RATE_PER_KG: float = 5.0

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__weight: float = 0.0
        self.weight = weight

    @property
    def weight(self) -> float:
        return self.__weight

    @weight.setter
    def weight(self, value: float) -> None:
        if not isfinite(value) or value < 0:
            raise ValueError("Weight must be finite and non-negative.")
        self.__weight = float(value)

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.weight * self.SHIPPING_RATE_PER_KG
