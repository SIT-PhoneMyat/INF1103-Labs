from pathlib import Path

path = Path("Week 4/inventory.txt") # idk why adding "Week 4" in the path can make it detectable
print("Path: ", path)

def load_inventory():
    if path.exists():   # if file exists
        print("Current Orders: \n")
        with path.open("r") as file:
            for line in file:
                print(line.strip())
            else:
                return int(line[:4])    # if orders exist, return last order id
    else:
        return None # if empty, the order id will start at 1001

def save_inventory(order):
    with path.open("a") as file:
        file.write("\n" + order)

last_order_id = load_inventory() 
# print("\nLast Order ID:", last_order_id)

while True:
    new_order_id = last_order_id + 1 if last_order_id is not None else 1001
    # print(f"\nNew Order ID: {new_order_id}")
    product_name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    order = f"{new_order_id}, {product_name}, {quantity}"
    save_inventory(order)

    print("New Order Added:")
    print(order)
    print("\nOrder successfully saved to orders.txt")

    cmd = input("\nDo you want to add more orders? (Y/n) Type quit/q/n to exit the program: ")
    if cmd.lower() == "quit" or cmd.lower() == 'n' or cmd.lower() == 'q':
        break
    
    last_order_id = new_order_id # item is added already, so the last order id is updated to the new order id

