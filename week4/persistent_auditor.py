# Week 4, Lab 4
import os

def load_inventory(filename="week4\\inventory.txt"):
    """
    Requirement: Reads existing orders from the file.
    Returns a list of orders. Each order is a dictionary: {'id': int, 'name': str, 'quantity': int}
    """
    orders = []
    
    if not os.path.exists(filename):
        return orders  # Return an empty list if file doesn't exist yet
        
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = [part.strip() for part in line.split(",")]
                if len(parts) == 3:
                    order_dict = {
                        "id": int(parts[0]),
                        "name": parts[1],
                        "quantity": int(parts[2])
                    }
                    orders.append(order_dict)
                    
    return orders

def save_inventory(total, history, filename="week4\\inventory.txt"):

    with open(filename, "w") as f:
        for order in orders_list:
            f.write(f"{order['id']}, {order['name']}, {order['quantity']}\n")
    print(f"\nOrder successfully saved to {filename.split('\\')[-1]}")

def get_valid_input(orders_list):

    product_name = input("Enter Product Name: ").strip()

    while True:
        qty_input = input("Enter Quantity: ").strip()
        if qty_input.isdigit() and int(qty_input) > 0:
            quantity = int(qty_input)
            break
            
        print("Error: Please enter a valid positive integer for quantity.")

    if orders_list:
        next_id = orders_list[-1]["id"] + 1
        
    return {"id": next_id, "name": product_name, "quantity": quantity}       

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    tax_amount = amount * 0.10
    return tax_amount

def generate_report(total_units, failed_attempts):
    print("\n----- Audit Report -----")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


# 1. Initialize variables
total_inventory, transaction_history = load_inventory()
failed_entries = 0

current_orders = load_inventory()
print("Current Orders:\n")
for order in current_orders:
    print(f"{order['id']}, {order['name']}, {order['quantity']}")

# 2. Continuous loop until user types 'quit'
while True:
    result = get_valid_input()

    if  result == 'quit':
        save_inventory(total_inventory, transaction_history)
        break
    elif result == 'invalid':
        failed_entries += 1
        continue

    stock_value = result

    transaction_history.append(stock_value)

    # Calculate the tax for this specific delivery
    delivery_tax = calculate_tax(stock_value)
    print(f"Tax for this delivery: ${delivery_tax:.2f}")

    # 6. Manage State: Add to running total
    total_inventory = process_delivery(total_inventory,stock_value)
    print(f"Added {stock_value} units. Current inventory: {total_inventory}")


generate_report(total_inventory, failed_entries)
    
