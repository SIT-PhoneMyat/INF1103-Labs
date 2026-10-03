from pathlib import Path

inventory = Path("inventory.json")

NEW_LINE = "\n"

def load_inventory() -> bool:
    pass

def save_inventory(product):
    pass

def add_product():
    print("Add New Product")
    product = {
        "product_id": input("Product ID: "),
        "product_name": input("Product Name: "),
        "price": float(input("Price: ")),
        "stock_quantity": int(input("Stock Quantity: "))
    }
    all_products.append(product)
    print(NEW_LINE + "Product added successfully!" + NEW_LINE)

def update_stock():
    pass

def search_product():
    pass

def display_all():
    if not all_products:
        print("No products in inventory." + NEW_LINE)
        return

    print("Current Inventory")
    print("------------------------------------------------")
    for product in all_products:
        print(f"ID: {product['product_id']} | Name: {product['product_name']} | Price: ${product['price']:.2f} | Stock: {product['stock_quantity']}")
    print("------------------------------------------------")
    print(NEW_LINE)


def save_and_exit():
    pass

all_products = [] # data will be loaded inside load_inventory()

while True:
    print("========================================")
    print("Inventory Management System")
    print("========================================" + NEW_LINE)

    if load_inventory():
        print("inventory.json found.")
        print("Inventory loaded successfully." + NEW_LINE)
    else:
        print("No existing inventory found.")
        print("Data will be saved to inventory.json file." + NEW_LINE)

    
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

    choice = input("Enter option: ")
    print(NEW_LINE)

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
            save_inventory(all_products)
        case "6":
            save_and_exit()
            break
        case _:
            print("Invalid option. Please try again.")