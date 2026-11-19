from math import isfinite

from Product import Product
from Supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, download_size: float,
                 supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.__download_size: float = 0.0
        self.download_size = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    @download_size.setter
    def download_size(self, value: float) -> None:
        if not isfinite(value) or value < 0:
            raise ValueError("Download size must be finite and non-negative.")
        self.__download_size = float(value)

    def display_information(self) -> None:
        super().display_information()
        print(f"Download size: {self.download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally by download."
