# Week 4, Lab 4
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH = os.path.join(BASE_DIR, "inventory.txt")

def load_inventory(filename="inventory.txt"):
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

def save_inventory(orders_list, filename="inventory.txt"):

    with open(filename, "w") as f:
        for order in orders_list:
            f.write(f"{order['id']}, {order['name']}, {order['quantity']}\n")
    clean_filename = filename.replace("\\", "/").split("/")[-1]
    print(f"\nOrder successfully saved to {clean_filename}")

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
    else:
        next_id = 1001
        
    return {"id": next_id, "name": product_name, "quantity": quantity}       


current_orders = load_inventory()
print("\nCurrent Orders:\n")
for order in current_orders:
    print(f"{order['id']}, {order['name']}, {order['quantity']}")

new_order = get_valid_input(current_orders)
current_orders.append(new_order)

print("\nNew Order Added:")
print(f"{new_order['id']},{new_order['name']},{new_order['quantity']}")
    
save_inventory(current_orders)