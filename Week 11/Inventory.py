from Product import Product


class Inventory:
    def __init__(self) -> None:
        # Products are supplied by the caller and can belong to other inventories.
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        return self.__products.copy()

    def add_product(self, product: Product) -> None:
        if self.find_product(product.product_id) is not None:
            raise ValueError("A product with this ID already exists.")
        self.__products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> list[Product]:
        return self.products

    def display_all_products(self) -> None:
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print()
