import csv
from pathlib import Path

from Inventory import Inventory
from ProductFactory import ProductFactory
from Supplier import Supplier


def load_products(path: str | Path, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            rows = csv.reader(file)
            header = next(rows, None)
            expected = ["product_type", "product_id", "name", "price", "stock_quantity"]
            if header != expected:
                print("Invalid CSV header. Expected: " + ",".join(expected))
            else:
                for row in rows:
                    try:
                        if len(row) != 5:
                            raise ValueError("Expected 5 columns.")
                        kind, product_id, name, price, stock = (value.strip() for value in row)
                        if not product_id or not name:
                            raise ValueError("Product ID and name must not be empty.")
                        product = ProductFactory.create(
                            kind, product_id, name, float(price), int(stock), supplier)
                        inventory.add_product(product)
                    except ValueError as error:
                        print(f"Skipping row {rows.line_num}: {error}")
                    else:
                        loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
