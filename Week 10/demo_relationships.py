"""Run this file to check the four Predict First answers without changing JSON."""

from DigitalProduct import DigitalProduct
from Inventory import Inventory
from Order import Order
from PhysicalProduct import PhysicalProduct
from main import show_product_details


def main() -> None:
    from Supplier import Supplier

    supplier = Supplier("S1", "Music Shop", "hello@music.example")
    physical = PhysicalProduct("P1", "Guitar", 200.0, 3, 2.5, supplier)
    digital = DigitalProduct("D1", "Music", 10.0, 20, 120.0, supplier)

    print("1. Association after del supplier")
    del supplier
    physical.supplier.display_information()
    digital.supplier.display_information()
    print("Same supplier:", physical.supplier is digital.supplier)

    print("\n2. Aggregation and transfer")
    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(physical)
    removed = inventory_a.remove_product("P1")
    print("Removed the original object:", removed is physical)
    physical.update_stock(8)
    show_product_details(physical)
    inventory_b.add_product(physical)
    print("Same object in B:", inventory_b.find_product("P1") is physical)

    print("\n3. Composition with a shared product")
    first_order = Order("O1")
    second_order = Order("O2")
    first_order.add_order_line(physical, 2)
    second_order.add_order_line(physical, 1)
    print("Same line:", first_order.order_lines[0] is second_order.order_lines[0])
    print("Same product:", first_order.order_lines[0].product
          is second_order.order_lines[0].product)
    first_order.add_order_line(digital, 3)
    first_order.display_information()
    first_order.remove_order_line(0)
    print("Total after removing the guitar line:", first_order.calculate_total())
    second_order.cancel()
    print("Cancelled order lines:", len(second_order.order_lines))
    print("Guitar still works:", physical.get_fulfilment_info())

    print("\n4. Polymorphism and LSP")
    inventory_b.add_product(digital)
    for product in inventory_b.products:
        product.update_stock(5)
        show_product_details(product)


if __name__ == "__main__":
    main()
