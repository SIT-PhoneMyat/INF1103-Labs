from math import isfinite

from DiscountStrategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be finite and between 0 and 100.")
        self.percentage = float(percentage)

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)
