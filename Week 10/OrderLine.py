from Product import Product


class OrderLine:
    """A line created and managed by its Order; its Product is independent."""

    def __init__(self, product: Product, quantity: int) -> None:
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Order quantity must be a positive whole number.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity
