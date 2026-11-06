from Product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from math import isfinite
from pathlib import Path
import json

# The main program shares one Inventory instance across all menu operations.
class Inventory:

    def __init__(self, inventory_path=None):
        self.__inventory = (Path(inventory_path) if inventory_path is not None
                            else Path(__file__).with_name("inventory.json"))
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
                if not product_id.strip() or not name.strip():
                    raise ValueError("Product ID and name cannot be empty.")
                if not isfinite(price) or price < 0 or stock < 0:
                    raise ValueError("Price and stock must be non-negative and finite.")
                product_type = product_data.get("type")
                if product_type == "physical":
                    extra_field = "weight"
                    product_class = PhysicalProduct
                elif product_type == "digital":
                    extra_field = "download_size"
                    product_class = DigitalProduct
                else:
                    raise ValueError("Each product needs a type of 'physical' or 'digital'.")
                extra_value = product_data[extra_field]
                if (type(extra_value) not in (int, float)
                        or not isfinite(extra_value) or extra_value < 0):
                    raise ValueError(f"{extra_field} must be a finite, non-negative number.")
                if any(product.product_id == product_id for product in products):
                    raise ValueError(f"Duplicate product ID: {product_id}")
                products.append(product_class(product_id, name, price, stock, extra_value))
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
            records = []
            for product in self.__all_products:
                record = {
                    "product_id": product.product_id,
                    "product_name": product.name,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                }
                if isinstance(product, PhysicalProduct):
                    record.update(type="physical", weight=product.weight)
                elif isinstance(product, DigitalProduct):
                    record.update(type="digital", download_size=product.download_size)
                else:
                    raise ValueError("Unsupported product type.")
                records.append(record)
            data = json.dumps(records, indent=4, allow_nan=False)
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
