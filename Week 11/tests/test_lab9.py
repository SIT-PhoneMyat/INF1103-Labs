import ast
import inspect
import io
import subprocess
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from BulkDiscount import BulkDiscount
from DiscountStrategy import DiscountStrategy
from Inventory import Inventory
from InventoryStorage import InventoryStorage
from NoDiscount import NoDiscount
from Order import Order
from OrderLine import OrderLine
from PercentageDiscount import PercentageDiscount
from ProductFactory import ProductFactory
from StudentDiscount import StudentDiscount
from Supplier import Supplier
from input_helpers import get_positive_float
from product_loader import load_products


class Lab9Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Lab", "lab@example.com")

    def product(self, kind="physical", **values):
        args = dict(product_id="P1", name="Example", price=125, stock_quantity=10,
                    supplier=self.supplier)
        args.update(values)
        return ProductFactory.create(kind, **args)

    def test_strategy_totals_switching_and_boundaries(self):
        order = Order("O1")
        order.add_order_line(self.product(), 2)
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250)
        for discount, expected in ((BulkDiscount(200, 20), 230),
                                   (PercentageDiscount(10), 225), (StudentDiscount(), 237.5)):
            order.set_discount(discount)
            self.assertEqual(order.calculate_total(), expected)
        self.assertEqual(BulkDiscount(200, 20).apply(199), 199)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)
        self.assertEqual(BulkDiscount(0, 20).apply(0), 0)
        self.assertEqual(PercentageDiscount(100).apply(250), 0)
        self.assertEqual(PercentageDiscount(0).apply(250), 250)

    def test_strategy_extension_and_shared_association(self):
        class FixedTotal(DiscountStrategy):
            def apply(self, total):
                return 42.0

        shared = PercentageDiscount(10)
        first, second = Order("A", shared), Order("B", shared)
        self.assertIs(first.discount, second.discount)
        first.set_discount(FixedTotal())
        self.assertEqual(first.calculate_total(), 42)
        self.assertIs(second.discount, shared)
        source = textwrap.dedent(inspect.getsource(Order.calculate_total))
        self.assertFalse(any(isinstance(node, ast.If) for node in ast.walk(ast.parse(source))))

    def test_invalid_discount_parameters(self):
        for value in (-1, 101, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                PercentageDiscount(value)
        for threshold, amount in ((-1, 1), (1, -1), (float("nan"), 1), (1, float("inf"))):
            with self.assertRaises(ValueError):
                BulkDiscount(threshold, amount)

    def test_factory_preserves_extra_fields_and_rejects_unknown(self):
        self.assertEqual(self.product(weight=2.5).weight, 2.5)
        self.assertEqual(self.product("digital", download_size=120).download_size, 120)
        self.assertEqual(self.product().weight, 0)
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            self.product("service")

    def test_unhandled_unknown_type_exits_with_traceback(self):
        script = ("from ProductFactory import ProductFactory; from Supplier import Supplier; "
                  "ProductFactory.create('service','S1','Installation',30,5,Supplier('S','Lab','e'))")
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                                cwd=Path(__file__).resolve().parents[1])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError: Unknown product type: service", result.stderr)
        self.assertIn("ProductFactory.py", result.stderr)

    def test_model_validation_and_lsp(self):
        for kind in ("physical", "digital"):
            for price in (0, -1, float("nan"), float("inf")):
                with self.subTest(kind=kind, price=price), self.assertRaises(ValueError):
                    self.product(kind, price=price)
            item = self.product(kind, stock_quantity=0)
            for quantity in (-1, 1.5, True):
                with self.assertRaises(ValueError):
                    item.update_stock(quantity)
                with self.assertRaises(ValueError):
                    self.product(kind, stock_quantity=quantity)
            with self.assertRaises(ValueError):
                item.price = 0
            for quantity in (0, -1, 1.5, True):
                with self.assertRaises(ValueError):
                    OrderLine(item, quantity)

    def test_price_retry_messages_and_finite_values(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as mocked:
            with redirect_stdout(output):
                self.assertEqual(get_positive_float("Price: "), 12.5)
        self.assertEqual(mocked.call_count, 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero."])
        with patch("builtins.input", side_effect=["nan", "inf", "0", "1"]):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 1)

    def test_sample_csv_output_and_continued_loading(self):
        output, inventory = io.StringIO(), Inventory()
        with redirect_stdout(output):
            load_products(Path(__file__).resolve().parents[1] / "products.csv",
                          inventory, self.supplier)
        self.assertEqual(output.getvalue().splitlines(), [
            "Skipping row 4: Unknown product type: service",
            "Skipping row 5: could not convert string to float: 'abc'",
            "3 products loaded.", "Load attempt finished."])
        self.assertEqual([p.product_id for p in inventory.products], ["P001", "D001", "P003"])

    def test_missing_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.csv"
            output = io.StringIO()
            with redirect_stdout(output):
                load_products(path, Inventory(), self.supplier)
            self.assertEqual(output.getvalue().splitlines(), [
                f"Products file not found: {path}", "Load attempt finished."])

    def test_csv_validation_duplicates_and_bad_header(self):
        header = "product_type,product_id,name,price,stock_quantity\n"
        body = ("physical,P1,Good,1,0\nphysical,P1,Duplicate,1,1\n"
                "digital,D1,Bad,0,1\nphysical,P2,Bad,1,-1\nshort,row\n"
                "digital,D2,Good,2,1\n")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.csv"
            path.write_text(header + body, encoding="utf-8")
            inventory, output = Inventory(), io.StringIO()
            with redirect_stdout(output):
                load_products(path, inventory, self.supplier)
            self.assertEqual(len(inventory.products), 2)
            self.assertEqual(output.getvalue().count("Skipping row"), 4)
            path.write_text("wrong,header\n", encoding="utf-8")
            with redirect_stdout(output := io.StringIO()):
                load_products(path, Inventory(), self.supplier)
            self.assertIn("Invalid CSV header.", output.getvalue())
            self.assertTrue(output.getvalue().endswith("0 products loaded.\nLoad attempt finished.\n"))

    def test_new_menu_actions(self):
        answers = ["14", "", "S1", "Lab", "lab@example.com", "8", "O1", "9", "O1",
                   "P001", "10", "13", "O1", "3", "200", "20", "10", "O1",
                   "13", "O1", "2", "10", "10", "O1", "6"]
        with tempfile.TemporaryDirectory() as folder:
            storage = InventoryStorage(Path(folder) / "inventory.json")
            with patch.object(main, "InventoryStorage", return_value=storage):
                with patch("builtins.input", side_effect=answers):
                    with redirect_stdout(output := io.StringIO()):
                        main.main()
            self.assertIn("Total: $230.00", output.getvalue())
            self.assertIn("Total: $225.00", output.getvalue())


if __name__ == "__main__":
    unittest.main()
