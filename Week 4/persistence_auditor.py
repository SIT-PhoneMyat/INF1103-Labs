from pathlib import Path

path = Path("Week 4/inventory.txt") # idk why adding "Week 4" in the path can make it detectable
print("Path: ", path)

def load_inventory():
    pass

def save_inventory():
    pass

while True:
    product_name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))

    cmd = input("\nDo you want to add more orders? (Y/n) Type quit/q/n to exit the program: ")
    if cmd.lower() == "quit" or cmd.lower() == 'n' or cmd.lower() == 'q':
        break

