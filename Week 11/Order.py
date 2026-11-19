from OrderLine import OrderLine
from Product import Product
from DiscountStrategy import DiscountStrategy
from NoDiscount import NoDiscount


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = NoDiscount() if discount is None else discount

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        # A read-only view prevents callers from inserting or transferring lines.
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        if index < 0 or index >= len(self.__order_lines):
            raise IndexError("Order line not found.")
        del self.__order_lines[index]

    def cancel(self) -> None:
        self.__order_lines.clear()

    def calculate_total(self) -> float:
        total = sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)
        return self.discount.apply(total)

    def display_information(self) -> None:
        print(f"Order: {self.order_id}")
        for index, line in enumerate(self.__order_lines, start=1):
            print(f"{index}. {line.product.name} x {line.quantity}: "
                  f"${line.calculate_subtotal():.2f}")
        print(f"Total: ${self.calculate_total():.2f}")
