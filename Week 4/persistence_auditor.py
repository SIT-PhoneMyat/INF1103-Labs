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

def save_inventory():
    pass

while True:
    product_name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))

    cmd = input("\nDo you want to add more orders? (Y/n) Type quit/q/n to exit the program: ")
    if cmd.lower() == "quit" or cmd.lower() == 'n' or cmd.lower() == 'q':
        break

