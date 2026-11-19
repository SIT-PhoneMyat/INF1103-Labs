from abc import ABC, abstractmethod
from math import isfinite

from Supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = 0.0
        self.__stock_quantity: int = 0
        self.__supplier: Supplier = supplier
        self.price = price
        self.update_stock(stock_quantity)

    @property
    def product_id(self) -> str:
        return self.__product_id

    @product_id.setter
    def product_id(self, value: str) -> None:
        self.__product_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if not isfinite(value) or value <= 0:
            raise ValueError("Price must be finite and greater than zero.")
        self.__price = float(value)

    @property
    def stock_quantity(self) -> int:
        return self.__stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value: int) -> None:
        self.update_stock(value)

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, new_quantity: int) -> None:
        if type(new_quantity) is not int or new_quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock_quantity = new_quantity

    def display_information(self) -> None:
        print(f"ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock_quantity}")
        self.supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
