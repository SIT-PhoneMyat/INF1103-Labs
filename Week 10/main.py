from math import isfinite

from DigitalProduct import DigitalProduct
from Inventory import Inventory
from InventoryStorage import InventoryStorage
from Order import Order
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def read_text(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        raise ValueError("This field cannot be empty.")
    return value


def read_number(prompt: str) -> float:
    value = float(input(prompt))
    if not isfinite(value) or value < 0:
        raise ValueError("Enter a finite, non-negative number.")
    return value


def add_product(inventory: Inventory) -> None:
    kind = input("Product type (1: Physical, 2: Digital): ").strip()
    if kind not in ("1", "2"):
        raise ValueError("Choose 1 or 2.")
    product_id = read_text("Product ID: ")
    if inventory.find_product(product_id) is not None:
        raise ValueError("A product with this ID already exists.")
    name = read_text("Product name: ")
    price = read_number("Price: ")
    stock = int(input("Stock quantity: "))
    extra = read_number("Weight (kg): " if kind == "1" else "Download size (MB): ")
    supplier_id = read_text("Supplier ID: ")
    supplier = next((p.supplier for p in inventory.products
                     if p.supplier.supplier_id == supplier_id), None)
    if supplier is None:
        supplier = Supplier(supplier_id, read_text("Supplier name: "),
                            read_text("Contact email: "))
    if kind == "1":
        product: Product = PhysicalProduct(product_id, name, price, stock, extra, supplier)
    else:
        product = DigitalProduct(product_id, name, price, stock, extra, supplier)
    inventory.add_product(product)
    print("Product added successfully!")


def require_product(inventory: Inventory) -> Product:
    product = inventory.find_product(read_text("Product ID: "))
    if product is None:
        raise ValueError("Product not found.")
    return product


def main() -> None:
    storage = InventoryStorage()
    try:
        inventory = storage.load()
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load inventory: {error}")
        print("Fix inventory.json before restarting. The file has been left alone.")
        return
    orders: dict[str, Order] = {}
    print("Inventory Management System")
    print("Orders are kept for this session. Products and suppliers are saved to JSON.")
    while True:
        print("\n1. Display all products\n2. Add product\n3. Update stock"
              "\n4. Search product\n5. Save inventory\n6. Exit"
              "\n7. Remove product\n8. Create order\n9. Add order line"
              "\n10. Display order\n11. Remove order line\n12. Cancel order")
        try:
            choice = input("Enter option: ").strip()
            if choice == "1":
                if not inventory.products:
                    print("No products in inventory.")
                inventory.display_all_products()
            elif choice == "2":
                add_product(inventory)
            elif choice == "3":
                product = require_product(inventory)
                product.update_stock(int(input("New stock quantity: ")))
                print("Stock updated successfully!")
            elif choice == "4":
                show_product_details(require_product(inventory))
            elif choice in ("5", "6"):
                storage.save(inventory)
                print("Inventory saved successfully.")
                if choice == "6":
                    break
            elif choice == "7":
                product = inventory.remove_product(read_text("Product ID: "))
                print("Product removed." if product is not None else "Product not found.")
            elif choice == "8":
                order_id = read_text("Order ID: ")
                if order_id in orders:
                    raise ValueError("This order ID already exists.")
                orders[order_id] = Order(order_id)
                print("Order created.")
            elif choice in ("9", "10", "11", "12"):
                order_id = read_text("Order ID: ")
                order = orders.get(order_id)
                if order is None:
                    raise ValueError("Order not found.")
                if choice == "9":
                    product = require_product(inventory)
                    order.add_order_line(product, int(input("Quantity: ")))
                    print("Order line added.")
                elif choice == "10":
                    order.display_information()
                elif choice == "11":
                    order.remove_order_line(int(input("Line number (starting at 1): ")) - 1)
                    print("Order line removed.")
                else:
                    order.cancel()
                    del orders[order_id]
                    print("Order cancelled.")
            else:
                print("Invalid option. Please try again.")
        except (ValueError, IndexError, OSError, UnicodeError) as error:
            print(f"Could not complete the operation: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended. Use Save or Exit to save inventory changes.")
            break


if __name__ == "__main__":
    main()
