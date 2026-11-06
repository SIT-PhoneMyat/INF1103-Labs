from CanBeShipped import CanBeShipped
from Product import Product


class PhysicalProduct(Product, CanBeShipped):
    # Product is the class parent; CanBeShipped defines the capability contract.
    SHIPPING_RATE_PER_KG = 5.0

    def __init__(self, product_id, name, price, stock_quantity, weight):
        super().__init__(product_id, name, price, stock_quantity)
        self.__weight = weight

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.weight * self.SHIPPING_RATE_PER_KG
