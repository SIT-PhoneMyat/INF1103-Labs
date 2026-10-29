from Inventory import Inventory
from Product import Product
from math import isfinite

NEW_LINE = "\n"

inventory = Inventory()  

print("========================================")
print("Inventory Management System")
print("========================================" + NEW_LINE)

inventory.load_inventory()

print("----------- MENU -----------")
print("1. Display All Products")
print("2. Add Product")
print("3. Update Stock")
print("4. Search Product")
print("5. Save Inventory")
print("6. Exit")
print("----------------------------")
print(NEW_LINE)

# Program while loop
while True:

    choice = input("Enter option: ")

    match choice:
        case "1":
            products = inventory.display_all()
            if not products:
                print("Inventory is empty.")
            for product in products:
                product.display_information()
                print(NEW_LINE)
        case "2":
            product_id = input("Enter product ID: ").strip()
            if not product_id:
                print("Product ID cannot be empty.")
                continue
            if inventory.search_product(product_id) is not None:
                print("A product with this ID already exists.")
                continue

            name = input("Enter product name: ").strip()
            if not name:
                print("Product name cannot be empty.")
                continue

            try:
                price = float(input("Enter product price: "))
                if not isfinite(price) or price < 0:
                    print("Price must be a finite, non-negative number.")
                    continue
                stock_quantity = int(input("Enter stock quantity: "))
                if stock_quantity < 0:
                    print("Stock quantity cannot be negative.")
                    continue
            except ValueError:
                print("Enter a valid price and a whole number for stock quantity.")
                continue

            product = Product(product_id, name, price, stock_quantity)
            inventory.add_product(product)
            print("Product added successfully.")
        case "3":
            product_id = input("Enter product ID: ").strip()
            product = inventory.search_product(product_id)
            if product is None:
                print("Product not found.")
                continue

            try:
                new_quantity = int(input("Enter new stock quantity: "))
                if new_quantity < 0:
                    print("Stock quantity cannot be negative.")
                    continue
            except ValueError:
                print("Stock quantity must be a whole number.")
                continue

            product.update_stock(new_quantity)
            print("Stock updated successfully.")
        case "4":
            product_id = input("Enter product ID: ").strip()
            product = inventory.search_product(product_id)
            if product is None:
                print("Product not found.")
            else:
                product.display_information()
        case "5":
            inventory.save_inventory()
        case "6":
            inventory.save_inventory()
            print("Goodbye!")
            break
        case _:
            print("Invalid option. Please try again.")
