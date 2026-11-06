from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface for any object that supports shipping."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass
