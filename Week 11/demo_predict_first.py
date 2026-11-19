"""Run the Predict First examples automatically, rather than opening the menu.

Run: python demo_predict_first.py
The numbered output corresponds to the questions in Predict_First_Notes.md.
Objects exist only for this run; nothing is saved to inventory.json.
"""

from pathlib import Path
from unittest.mock import patch

from BulkDiscount import BulkDiscount
from Inventory import Inventory
from Order import Order
from PercentageDiscount import PercentageDiscount
from ProductFactory import ProductFactory
from StudentDiscount import StudentDiscount
from Supplier import Supplier
from input_helpers import get_positive_float
from product_loader import load_products


def main() -> None:
    supplier = Supplier("S1", "Lab Supplier", "hello@example.com")
    # Arguments after the type are ID, name, price, stock, and supplier.
    product = ProductFactory.create("physical", "P1", "Example", 125, 10, supplier)
    order = Order("O1", BulkDiscount(200, 20))
    order.add_order_line(product, 2)
    # The subtotal is 125 * 2 = 250. Each calculation starts from that subtotal.
    print("1 and 2. Strategy extension and totals")
    print("Bulk:", order.calculate_total())
    order.set_discount(PercentageDiscount(10))
    print("Percentage:", order.calculate_total())
    order.set_discount(StudentDiscount())
    print("Student:", order.calculate_total())

    print("\n3. Shared strategy association")
    shared = PercentageDiscount(10)
    first, second = Order("A", shared), Order("B", shared)
    # "is" checks whether these are the SAME object, not just equal values.
    print("Same strategy:", first.discount is second.discount)
    first.set_discount(StudentDiscount())
    print("Second still uses shared strategy:", second.discount is shared)

    print("\n4. Unknown product type (caught for this demo)")
    # Deliberately request an unsupported type. Catch it so the demo can continue.
    try:
        ProductFactory.create("service", "S1", "Installation", 30, 5, supplier)
    except ValueError as error:
        print(f"{type(error).__name__}: {error}")

    print("\n5. Factory creation sites")
    # This question is checked by inspecting the source; these lines explain it.
    print("Production product construction is centralised in ProductFactory.create().")
    print("JSON save schema and menu choices still require explicit support for a new type.")

    print("\n6. LSP stock validation")
    for kind in ("physical", "digital"):
        item = ProductFactory.create(kind, kind, kind, 1, 0, supplier)
        try:
            # Both subclasses must reject the same invalid stock value.
            item.update_stock(-1)
        except ValueError as error:
            print(f"{kind}: {error}")

    print("\n7. Input abc, -5, 12.50")
    # Temporarily replace input(): its first three calls return these strings.
    # No typing is needed. Normal input() is restored when the "with" block ends.
    # The helper rejects the first two answers and returns float 12.5 for the third.
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        value = get_positive_float("Price: ")
    print("Returned:", value)

    print("\n8a. Supplied CSV")
    # __file__ is this script's path. with_name finds the CSV beside this script,
    # even when the command is run from another folder. Inventory() is fresh/empty.
    load_products(Path(__file__).with_name("products.csv"), Inventory(), supplier)
    print("\n8b. Missing CSV (equivalent to renaming it)")
    # This filename deliberately does not exist; we do not rename the real CSV.
    load_products("products_missing.csv", Inventory(), supplier)


if __name__ == "__main__":
    # Run main() only when this file is executed, not when it is imported.
    main()
