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
            print(NEW_LINE)
            products = inventory.display_all()
            if not products:
                print("No products in inventory." + NEW_LINE)
                print("------------------------------------------------" + NEW_LINE)
                continue
            print(NEW_LINE + "Current Inventory")
            print("------------------------------------------------")
            for product in products:
                print(f"ID: {product.product_id} | Name: {product.name} | Price: ${product.price:.2f} | Stock: {product.stock_quantity}")
            print("------------------------------------------------")
            print(NEW_LINE)
        case "2":
            print(NEW_LINE + "Add New Product")
            product_id = input("Product ID: ").strip()
            if not product_id:
                print("Product ID cannot be empty.")
                continue
            if inventory.search_product(product_id) is not None:
                print("A product with this ID already exists.")
                continue

            name = input("Product Name: ").strip()
            if not name:
                print("Product name cannot be empty.")
                continue

            try:
                price = float(input("Price: "))
                if not isfinite(price) or price < 0:
                    print("Price must be a finite, non-negative number.")
                    continue
                stock_quantity = int(input("Stock Quantity: "))
                if stock_quantity < 0:
                    print("Stock quantity cannot be negative.")
                    continue
            except ValueError:
                print("Enter a valid price and a whole number for stock quantity.")
                continue

            product = Product(product_id, name, price, stock_quantity)
            inventory.add_product(product)
            print(NEW_LINE + "Product added successfully!" + NEW_LINE)
        case "3":
            print(NEW_LINE + "Update Stock")
            product_id = input("Enter Product ID: ").strip()
            print(NEW_LINE)
            products = inventory.display_all()
            matches = [product for product in products if product.product_id == product_id]
            if not products:
                print("No items in the inventory.")
            elif not matches:
                print("Product not found.")
            for product in matches:
                print("Product Found:")
                print("Name: " + product.name)
                print("Current Stock: " + str(product.stock_quantity))
                print(NEW_LINE)
                try:
                    new_quantity = int(input("New Stock Quantity: "))
                    if new_quantity < 0:
                        print("Stock quantity cannot be negative.")
                        continue
                except ValueError:
                    print("Stock quantity must be a whole number.")
                    continue
                product.update_stock(new_quantity)
                print(NEW_LINE)
                print("Stock updated successfully!")
            print(NEW_LINE)
        case "4":
            print(NEW_LINE + "Search Product")
            product_id = input("Enter Product ID: ").strip()
            matches = [product for product in inventory.display_all() if product.product_id == product_id]
            for product in matches:
                print(NEW_LINE + "Product Found")
                print("------------------------------------------------")
                product.display_information()
                print("------------------------------------------------")
            if not matches:
                print("Product with ID " + product_id + " is not found.")
            print(NEW_LINE)
        case "5":
            inventory.save_inventory()
        case "6":
            if not inventory.save_inventory():
                continue
            print("Program is now terminating...")
            print(NEW_LINE + "Thank you for using Inventory Management System.")
            print("Program terminated.")
            print(NEW_LINE)
            break
        case _:
            print("Invalid option. Please try again.")
