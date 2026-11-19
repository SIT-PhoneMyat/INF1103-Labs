from math import isfinite

from DiscountStrategy import DiscountStrategy


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if not isfinite(threshold) or threshold < 0:
            raise ValueError("Threshold must be finite and non-negative.")
        if not isfinite(amount) or amount < 0:
            raise ValueError("Discount amount must be finite and non-negative.")
        self.threshold = float(threshold)
        self.amount = float(amount)

    def apply(self, total: float) -> float:
        # A discount cannot turn a non-negative order total into a debt.
        return max(0.0, total - self.amount) if total >= self.threshold else total
