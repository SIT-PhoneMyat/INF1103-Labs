from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, *, weight: float = 0.0,
               download_size: float = 0.0) -> Product:
        # The lab CSV omits weight and download size. Zero means unspecified;
        # menu input and saved JSON still preserve their actual values.
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, weight, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, download_size, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
