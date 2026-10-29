from Product import Product
from pathlib import Path
import json

# The main program shares one Inventory instance across all menu operations.
class Inventory:

    def __init__(self, inventory_path="inventory.json"):
        self.__inventory = Path(inventory_path)
        self.__all_products: list[Product] = []
        self.__load_failed = False

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
        try:
            with self.__inventory.open("r", encoding="utf-8") as f:
                print("inventory.json found.")
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Inventory must contain a list of products.")
            products = []
            for product_data in data:
                if not isinstance(product_data, dict):
                    raise ValueError("Each product must be an object.")
                # Accept files from both the procedural and earlier OOP versions.
                name = (product_data["product_name"] if "product_name" in product_data
                        else product_data["name"])
                product_id = product_data["product_id"]
                price = product_data["price"]
                stock = product_data["stock_quantity"]
                if (not isinstance(product_id, str) or not isinstance(name, str)
                        or type(price) not in (int, float) or type(stock) is not int):
                    raise ValueError("Product fields have invalid types.")
                products.append(Product(product_id, name, price, stock))
            # Replace only after every record has loaded successfully.
            self.__all_products = products
            self.__load_failed = False
            print("Inventory loaded successfully.\n")
            return True
        except FileNotFoundError:
            self.__load_failed = False
            print("No existing inventory found.")
            print("Data will be saved to inventory.json file.\n")
            return True
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
            self.__load_failed = True
            print("There was an error loading the inventory.")
            print(f"Details: {error}\n")
            return False

    def save_inventory(self):
        print("\nSaving inventory...")
        try:
            if self.__load_failed:
                print("Inventory was not saved because loading failed. Fix the file and reload first.")
                return False
            if not self.__all_products:
                print("Empty inventory. Please add a new product to save.")
                return True
            data = json.dumps([
                {
                    "product_id": product.product_id,
                    "product_name": product.name,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                }
                for product in self.__all_products
            ], indent=4)
            with self.__inventory.open("w", encoding="utf-8") as f:
                f.write(data)
            print("Inventory saved successfully to inventory.json.")
            return True
        except (OSError, UnicodeError, TypeError, ValueError) as error:
            print("There was an error saving the data to file.")
            print(f"Details: {error}")
            return False
        finally:
            print("\n")
