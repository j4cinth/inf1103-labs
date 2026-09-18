# Week 2, Lab 2

def get_valid_input():

    while True:
        user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()
        # Check if user wants to quit
        if user_input.lower() == 'quit':
            return 'quit'
        
         # 4. Handle invalid input: Reject letters and punctuation
        elif not user_input.isdigit() and not (user_input.startswith("-") and user_input[1:].isdigit()):
            print("Error: Invalid entry. Please enter a valid integer.")
            return 'invalid'
        else:
            stock_value = int(user_input)
            # 5. Enforce business rules: Reject negative numbers
            if stock_value < 0:
                    print("Error: Negative values are not allowed.")
                    return 'invalid'
            else:
                return stock_value

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax_amount = amount * 0.10
    return tax_amount


# 1. Initialize variables
total_inventory = 0
failed_entries = 0

# 2. Continuous loop until user types 'quit'
while True:
    result = get_valid_input()

    if  result == 'quit':
        break
    elif result == 'invalid':
        failed_entries += 1
        continue

    stock_value = result

    # Calculate the tax for this specific delivery
    delivery_tax = calculate_tax(stock_value)
    print(f"Tax for this delivery: ${delivery_tax:.2f}")

    # 6. Manage State: Add to running total
    total_inventory = process_delivery(total_inventory,stock_value)
    print(f"Added {stock_value} units. Current inventory: {total_inventory}")

    
# 8. Reporting when the loop exits
print("\n--- Audit Report ---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")

    
