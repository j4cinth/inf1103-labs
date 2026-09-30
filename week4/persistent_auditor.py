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


total_inventory, transaction_history = load_inventory()
failed_entries = 0

current_orders = load_inventory()
print("Current Orders:\n")
for order in current_orders:
    print(f"{order['id']}, {order['name']}, {order['quantity']}")

new_order = get_valid_input(current_orders)
current_orders.append(new_order)

print("\nNew Order Added:")
print(f"{new_order['id']},{new_order['name']},{new_order['quantity']}")
    
save_inventory(current_orders)