inventory=0
failed_entries = 0

while True:
    stock_quantity = input("Enter stock quantity: ")

    if stock_quantity.lower() == "quit":
        break

    elif stock_quantity.startswith("-") and stock_quantity[1:].isdigit():
        print("Invalid input. Stock quantity cannot be negative.")
        failed_entries += 1
        continue

    elif not stock_quantity.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    else:
        inventory += int(stock_quantity)

print("\n--- Daily Delivery Report ---")
print(f"Total Units Processed: {inventory}")
print(f"Failed Entries: {failed_entries}")