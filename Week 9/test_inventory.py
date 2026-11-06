import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main

from CanBeShipped import CanBeShipped
from DigitalProduct import DigitalProduct
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from Product import Product


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "inventory.json"
        self.inventory = Inventory(self.path)
        self.physical = PhysicalProduct("P1", "Guitar", 200, 3, 2.5)
        self.digital = DigitalProduct("D1", "Music", 10, 20, 120)
        self.output = io.StringIO()
        self.stdout = redirect_stdout(self.output)
        self.stdout.__enter__()
        self.addCleanup(self.stdout.__exit__, None, None, None)

    def test_abstract_contracts(self):
        with self.assertRaises(TypeError):
            Product("P0", "Generic", 1, 1)
        with self.assertRaises(TypeError):
            CanBeShipped()

        class MissingShipping(Product, CanBeShipped):
            def get_fulfilment_info(self):
                return "Shipping"

        with self.assertRaises(TypeError):
            MissingShipping("P0", "Incomplete", 1, 1)

    def test_display_inherits_common_information(self):
        for product, extra in [(self.physical, "Weight: 2.5 kg"),
                               (self.digital, "Download size: 120 MB")]:
            self.output.seek(0)
            self.output.truncate()
            product.display_information()
            output = self.output.getvalue()
            for expected in [product.product_id, product.name,
                             str(product.price), str(product.stock_quantity), extra]:
                self.assertIn(expected, output)

    def test_fulfilment_and_shipping(self):
        self.assertIn("shipping", self.physical.get_fulfilment_info())
        self.assertIn("digitally", self.digital.get_fulfilment_info())
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))
        for weight, expected in [(0, 0), (1, 5), (2.5, 12.5)]:
            self.physical.weight = weight
            self.assertEqual(self.physical.calculate_shipping_cost(), expected)

    def test_inventory_operations_and_round_trip(self):
        self.assertTrue(self.inventory.load_inventory())
        self.inventory.add_product(self.physical)
        self.inventory.add_product(self.digital)
        self.assertEqual(len(self.inventory.display_all()), 2)
        self.assertIs(self.inventory.search_product("P1"), self.physical)
        self.assertIsNone(self.inventory.search_product("missing"))
        self.physical.update_stock(8)
        self.assertTrue(self.inventory.save_inventory())
        records = json.loads(self.path.read_text())
        self.assertEqual([record["type"] for record in records], ["physical", "digital"])

        restored = Inventory(self.path)
        self.assertTrue(restored.load_inventory())
        physical = restored.search_product("P1")
        digital = restored.search_product("D1")
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual((physical.name, physical.price, physical.stock_quantity,
                          physical.weight), ("Guitar", 200, 8, 2.5))
        self.assertEqual((digital.name, digital.price, digital.stock_quantity,
                          digital.download_size), ("Music", 10, 20, 120))
        self.assertEqual(physical.calculate_shipping_cost(), 12.5)
        self.assertTrue(restored.load_inventory())
        self.assertEqual(len(restored.display_all()), 2)

    def test_invalid_file_does_not_replace_inventory_or_get_overwritten(self):
        self.inventory.add_product(self.physical)
        for contents in ['{broken', '[{"type": "unknown"}]',
                         json.dumps([{"product_id": "old", "name": "Legacy",
                                      "price": 1, "stock_quantity": 1}])]:
            self.path.write_text(contents)
            self.assertFalse(self.inventory.load_inventory())
            self.assertEqual(self.inventory.display_all(), [self.physical])
            self.assertFalse(self.inventory.save_inventory())
            self.assertEqual(self.path.read_text(), contents)

    def test_menu_add_update_search_save_and_restart(self):
        answers = ["2", "1", "P1", "Guitar", "200", "3", "2.5",
                   "2", "2", "D1", "Music", "10", "20", "120",
                   "3", "P1", "8", "4", "D1", "1", "5", "6"]
        with patch.object(main, "Inventory", return_value=self.inventory):
            with patch("builtins.input", side_effect=answers):
                main.main()
        restored = Inventory(self.path)
        self.output.seek(0)
        self.output.truncate()
        with patch.object(main, "Inventory", return_value=restored):
            with patch("builtins.input", side_effect=["1", "6"]):
                main.main()
        output = self.output.getvalue()
        for expected in ["Weight: 2.5 kg", "Download size: 120.0 MB",
                         "Stock: 8", "Shipping cost: $12.50"]:
            self.assertIn(expected, output)


if __name__ == "__main__":
    unittest.main()
