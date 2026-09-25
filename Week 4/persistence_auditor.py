from pathlib import Path

path = Path("inventory.txt") # idk why adding "Week 4" in the path can make it detectable
print("Path: ", path)

def load_inventory():
    if path.exists():   # if file exists
        print("Current Orders: \n")
        order_id = 1000 # if file exists but empty, the order id will start at 1001
        with path.open("r") as file:
            for line in file:
                if line.strip() != "": # we are skipping empty lines
                    print(line.strip()) 
                    order_id = int(line[:4])  # Update order_id with the last seen order ID
        return order_id
    else:
        print("Current Orders: \n")
        return None # if empty, the order id will start at 1001

def save_inventory(order):
    with path.open("a") as file:
        file.write("\n" + order)

last_order_id = load_inventory() 
# print("\nLast Order ID:", last_order_id)

while True:
    new_order_id = last_order_id + 1 if last_order_id is not None else 1001
    # print(f"\nNew Order ID: {new_order_id}")
    print("\n" + "-"*20)
    product_name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    order = f"{new_order_id}, {product_name}, {quantity}"
    save_inventory(order)

    print("\nNew Order Added:")
    print(order)
    print("\nOrder successfully saved to orders.txt")
    print("-"*20)

    cmd = input("\nDo you want to add more orders? (Y/n) Type quit/q/n to exit the program: ")
    if cmd.lower() == "quit" or cmd.lower() == 'n' or cmd.lower() == 'q':
        break
    
    last_order_id = new_order_id # item is added already, so the last order id is updated to the new order id

