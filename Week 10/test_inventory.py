import io
import json
import tempfile
import unittest
import weakref
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from CanBeShipped import CanBeShipped
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from InventoryStorage import InventoryStorage
from Order import Order
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Music Shop", "hello@music.example")
        self.physical = PhysicalProduct("P1", "Guitar", 200, 3, 2.5, self.supplier)
        self.digital = DigitalProduct("D1", "Music", 10, 20, 120, self.supplier)

    def test_association_survives_supplier_variable_deletion(self) -> None:
        supplier = self.supplier
        reference = weakref.ref(supplier)
        del self.supplier
        del supplier
        self.assertIs(self.physical.supplier, reference())
        self.assertIs(self.physical.supplier, self.digital.supplier)
        output = io.StringIO()
        with redirect_stdout(output):
            self.physical.supplier.display_information()
            self.digital.supplier.display_information()
        self.assertEqual(output.getvalue().count("Music Shop"), 2)

    def test_aggregation_preserves_identity_across_transfer(self) -> None:
        first, second = Inventory(), Inventory()
        first.add_product(self.physical)
        self.assertIs(first.remove_product("P1"), self.physical)
        self.assertIsNone(first.find_product("P1"))
        self.physical.update_stock(8)
        second.add_product(self.physical)
        del first
        self.assertIs(second.find_product("P1"), self.physical)
        self.assertEqual(self.physical.stock_quantity, 8)
        self.assertIsNone(second.remove_product("missing"))
        with self.assertRaises(ValueError):
            second.add_product(self.physical)

    def test_composition_has_distinct_lines_and_shared_product(self) -> None:
        first, second = Order("O1"), Order("O2")
        first.add_order_line(self.physical, 2)
        second.add_order_line(self.physical, 1)
        self.assertIsNot(first.order_lines[0], second.order_lines[0])
        self.assertIs(first.order_lines[0].product, second.order_lines[0].product)
        first.add_order_line(self.digital, 3)
        self.assertEqual(first.calculate_total(), 430.0)
        line_reference = weakref.ref(first.order_lines[0])
        first.remove_order_line(0)
        self.assertIsNone(line_reference())
        self.assertEqual(first.calculate_total(), 30.0)
        second.cancel()
        self.assertEqual(second.order_lines, ())
        self.assertEqual(second.calculate_total(), 0.0)
        self.assertEqual(self.physical.price, 200.0)
        with self.assertRaises(ValueError):
            first.add_order_line(self.digital, 0)

    def test_lsp_and_polymorphism(self) -> None:
        with self.assertRaises(TypeError):
            Product("P0", "Abstract", 1, 1, self.supplier)
        inventory = Inventory()
        for product in (self.physical, self.digital):
            inventory.add_product(product)
            product.update_stock(5)
            self.assertEqual(product.stock_quantity, 5)
            with self.assertRaises(ValueError):
                product.update_stock(-1)
        output = io.StringIO()
        with redirect_stdout(output):
            inventory.display_all_products()
            for product in inventory.products:
                main.show_product_details(product)
        for expected in ("Weight: 2.5 kg", "Download size: 120.0 MB",
                         "requires physical shipping", "delivered digitally by download"):
            self.assertIn(expected, output.getvalue())
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertEqual(self.physical.calculate_shipping_cost(), 12.5)

    def test_storage_round_trip_shared_supplier_and_empty_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            storage = InventoryStorage(Path(folder) / "inventory.json")
            inventory = storage.load()
            inventory.add_product(self.physical)
            inventory.add_product(self.digital)
            storage.save(inventory)
            restored = storage.load()
            physical = restored.find_product("P1")
            digital = restored.find_product("D1")
            self.assertIsInstance(physical, PhysicalProduct)
            self.assertIsInstance(digital, DigitalProduct)
            self.assertIs(physical.supplier, digital.supplier)
            self.assertEqual((physical.weight, digital.download_size), (2.5, 120))
            restored.remove_product("P1")
            restored.remove_product("D1")
            storage.save(restored)
            self.assertEqual(json.loads(storage.path.read_text()), [])

    def test_invalid_storage_is_not_overwritten_at_startup(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            storage = InventoryStorage(Path(folder) / "inventory.json")
            storage.path.write_text("{broken", encoding="utf-8")
            with patch.object(main, "InventoryStorage", return_value=storage):
                with redirect_stdout(io.StringIO()):
                    main.main()
            self.assertEqual(storage.path.read_text(), "{broken")

    def test_menu_inventory_and_orders(self) -> None:
        answers = ["2", "1", "P1", "Guitar", "200", "3", "2.5",
                   "S1", "Music Shop", "hello@music.example",
                   "2", "2", "D1", "Music", "10", "20", "120", "S1",
                   "3", "P1", "8", "4", "D1", "8", "O1",
                   "9", "O1", "P1", "2", "9", "O1", "D1", "3",
                   "10", "O1", "11", "O1", "1", "10", "O1",
                   "12", "O1", "7", "P1", "1", "5", "6"]
        with tempfile.TemporaryDirectory() as folder:
            storage = InventoryStorage(Path(folder) / "inventory.json")
            output = io.StringIO()
            with patch.object(main, "InventoryStorage", return_value=storage):
                with patch("builtins.input", side_effect=answers):
                    with redirect_stdout(output):
                        main.main()
            self.assertIn("Total: $430.00", output.getvalue())
            self.assertIn("Total: $30.00", output.getvalue())
            self.assertIsNone(storage.load().find_product("P1"))
            self.assertIsNotNone(storage.load().find_product("D1"))


if __name__ == "__main__":
    unittest.main()
