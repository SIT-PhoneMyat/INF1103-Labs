from Product import Product
from pathlib import Path
import json

# This class should be a Singleton class, meaning only one instance of this class should exist throughout the program.
# Otherwise, if multiple instances of this class are created, it will lead to data inconsistency and unexpected behavior.
class Inventory:

    def __init__(self, inventory_path="inventory.json"):
        self.__inventory = Path(inventory_path)
        self.__all_products: list[Product] = [] # Just to reference the type of the list, not to create a new list

    def add_product(self, product):
        self.__all_products.append(product)

    def search_product(self, product_id):
        for product in self.__all_products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self):
        return self.__all_products

    # Utility methods below

    def load_inventory(self):
        if self.__inventory.exists():
            print("inventory.json found.")
            with self.__inventory.open("r", encoding="utf-8") as f:
                data = json.load(f)
                for product_data in data:
                    product = Product(
                        product_id=product_data["product_id"],
                        name=product_data["name"],
                        price=product_data["price"],
                        stock_quantity=product_data["stock_quantity"]
                    )
                    self.__all_products.append(product)
            print("Inventory loaded successfully.\n")

    def save_inventory(self):
        with self.__inventory.open("w", encoding="utf-8") as f:
            json.dump([
                {
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                }
                for product in self.__all_products
            ], f, indent=4)
        print("Inventory saved successfully.\n")
