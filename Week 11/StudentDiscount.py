from DiscountStrategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """A fourth strategy: a fixed five percent student discount."""

    def apply(self, total: float) -> float:
        return total * 0.95
