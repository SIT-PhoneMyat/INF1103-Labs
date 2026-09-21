inventory=0
failed_entries = 0
deliveries_processed = 0

def get_valid_input(prompt):
    global failed_entries

    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == "quit":
            return "quit"
        elif user_input.startswith("-") and user_input[1:].isdecimal():
            print("Invalid input. Stock quantity cannot be negative.")
            failed_entries += 1
        elif not user_input.isdecimal():
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
        else:
            return int(user_input)

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("\n--- Daily Delivery Report ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

while True:
    stock_quantity = get_valid_input("Enter stock quantity (type 'quit' to exit): ")

    if stock_quantity == "quit":
        break

    inventory = process_delivery(inventory, stock_quantity)
    delivery_tax = calculate_tax(stock_quantity)
    deliveries_processed += 1
    print(f"Tax for this delivery: {delivery_tax:.2f}")

generate_report(inventory, failed_entries)