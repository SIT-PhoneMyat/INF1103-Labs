from pathlib import Path
import json

inventory = Path("inventory.json")

NEW_LINE = "\n"

def load_inventory() -> bool:
    if inventory.exists():
        print("inventory.json found.")
        with inventory.open("r", encoding="utf-8") as f:
            global all_products
            all_products = json.load(f)
        
        print("Inventory loaded successfully." + NEW_LINE)
    else:
        print("No existing inventory found.")
        print("Data will be saved to inventory.json file." + NEW_LINE)

def save_inventory():
    print(NEW_LINE + "Saving inventory...")
    try:
        # all_products will have existing data (on program startup) + new data. 
        # if JSON file has data but all_products is empty by somehow, running this method will overwrite JSON with empty data
        # to prevent this, save only if all_products has data, (make sure all data is loaded on startup)
        if all_products: 
            with inventory.open("w") as file:
                file.write(json.dumps(all_products, indent=4))
            print("Inventory saved successfully to inventory.json.")
        else:
            print("Empty inventory. Please add a new product to save.")

    except json.JSONDecodeError as e:
        print("There was an error saving the data to file.")
        print("Details: " + e)

    print(NEW_LINE)
    

def add_product():
    print(NEW_LINE + "Add New Product")
    product = {
        "product_id": input("Product ID: "),
        "product_name": input("Product Name: "),
        "price": float(input("Price: ")),
        "stock_quantity": int(input("Stock Quantity: "))
    }
    all_products.append(product)
    print(NEW_LINE + "Product added successfully!" + NEW_LINE)

def update_stock():
    print(NEW_LINE + "Update Stock")
    product_id = input("Enter Product ID: ")
    print(NEW_LINE)

    if all_products:
        has_found = False
        for product in all_products:
            if product.get("product_id") == product_id:
                has_found = True
                print("Product Found:")
                print("Name: " + product.get("product_name"))
                print("Current Stock: " + str(product.get("stock_quantity")))

                print(NEW_LINE)
                product["stock_quantity"] = int(input("New Stock Quantity: "))
                print(NEW_LINE)
                print("Stock updated successfully!")

        if not has_found:
            print("Product not found.")
    else:
        print("No items in the inventory.")
    print(NEW_LINE)


def search_product():
    print(NEW_LINE + "Search Product")
    product_id = input("Enter Product ID: ")
    has_found = False

    for product in all_products:
        if product.get("product_id") == product_id:
            has_found = True
            print(NEW_LINE + "Product Found")
            print("------------------------------------------------")
            print("ID: " + product.get("product_id"))
            print("Name: " + product.get("product_name"))
            print("Price: " + str(product.get("price")))
            print("Stock: " + str(product.get("stock_quantity")))
            print("------------------------------------------------")

    if not has_found:
        print("Product with ID " + product_id + " is not found.")
    
    print(NEW_LINE)


def display_all():
    print(NEW_LINE)
    if not all_products:
        print("No products in inventory." + NEW_LINE)
        print("------------------------------------------------" + NEW_LINE)
        return

    print(NEW_LINE + "Current Inventory")
    print("------------------------------------------------")
    for product in all_products:
        print(f"ID: {product['product_id']} | Name: {product['product_name']} | Price: ${product['price']:.2f} | Stock: {product['stock_quantity']}")
    print("------------------------------------------------")
    print(NEW_LINE)


def save_and_exit():
    save_inventory()
    print("Program is now terminating...")

    print(NEW_LINE + "Thank you for using Inventory Management System.")
    print("Program terminated.")
    print(NEW_LINE)

all_products = [] # data will be loaded inside load_inventory()

print("========================================")
print("Inventory Management System")
print("========================================" + NEW_LINE)

load_inventory()

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
            display_all()
        case "2":
            add_product()
        case "3":
            update_stock()
        case "4":
            search_product()
        case "5":
            save_inventory()
        case "6":
            save_and_exit()
            break
        case _:
            print("Invalid option. Please try again.")