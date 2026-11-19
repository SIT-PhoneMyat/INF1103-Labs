"""JSON conversion lives here so Inventory only needs the Product interface."""

import json
from pathlib import Path

from DigitalProduct import DigitalProduct
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier
from ProductFactory import ProductFactory


class InventoryStorage:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path: Path = (Path(path) if path is not None
                           else Path(__file__).with_name("inventory.json"))

    def load(self) -> Inventory:
        inventory = Inventory()
        if not self.path.exists():
            return inventory
        records = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            raise ValueError("Inventory must contain a list of products.")
        suppliers: dict[str, Supplier] = {}
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Each product must be an object.")
            data = record["supplier"]
            if not isinstance(data, dict):
                raise ValueError("Each product needs supplier details.")
            supplier_id = data["supplier_id"]
            if not all(isinstance(data[key], str) and data[key].strip()
                       for key in ("supplier_id", "name", "contact_email")):
                raise ValueError("Supplier details must be non-empty text.")
            if supplier_id in suppliers:
                supplier = suppliers[supplier_id]
                if (supplier.name, supplier.contact_email) != (data["name"], data["contact_email"]):
                    raise ValueError("Conflicting details for the same supplier ID.")
            else:
                supplier = Supplier(supplier_id, data["name"], data["contact_email"])
                suppliers[supplier_id] = supplier
            name = record.get("product_name", record.get("name"))
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Product name must be non-empty text.")
            if not isinstance(record["product_id"], str) or not record["product_id"].strip():
                raise ValueError("Product ID must be non-empty text.")
            if type(record["price"]) not in (int, float):
                raise ValueError("Price must be a number.")
            product: Product
            common = (record["product_id"], name, record["price"], record["stock_quantity"])
            if record["type"] == "physical":
                product = ProductFactory.create("physical", *common, supplier,
                                                weight=record["weight"])
            elif record["type"] == "digital":
                product = ProductFactory.create("digital", *common, supplier,
                                                download_size=record["download_size"])
            else:
                raise ValueError("Unknown product type.")
            inventory.add_product(product)
        return inventory

    def save(self, inventory: Inventory) -> None:
        records: list[dict[str, object]] = []
        for product in inventory.products:
            supplier = product.supplier
            record: dict[str, object] = {
                "product_id": product.product_id,
                "product_name": product.name,
                "price": product.price,
                "stock_quantity": product.stock_quantity,
                "supplier": {"supplier_id": supplier.supplier_id,
                             "name": supplier.name,
                             "contact_email": supplier.contact_email},
            }
            # Only serialization needs to know the concrete file schema.
            if isinstance(product, PhysicalProduct):
                record.update(type="physical", weight=product.weight)
            elif isinstance(product, DigitalProduct):
                record.update(type="digital", download_size=product.download_size)
            else:
                raise ValueError("No JSON format defined for this product type.")
            records.append(record)
        text = json.dumps(records, indent=4, allow_nan=False)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(text + "\n", encoding="utf-8")
        temporary.replace(self.path)
