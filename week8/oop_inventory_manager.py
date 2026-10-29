import os
import json

FILENAME = "inventory.json"

class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity: int):
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock


def get_non_empty_input(prompt_text):
    """Repeatedly prompts user until a non-empty string is provided."""
    while True:
        user_input = input(prompt_text).strip()
        if user_input:
            return user_input
        print("Error: Input cannot be empty. Please try again.")

def get_positive_number(prompt_text, is_int=False):
    """Repeatedly prompts user until a valid positive number is provided."""
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            print("Error: Input cannot be empty.")
            continue
        try:
            if is_int:
                val = int(user_input)
            else:
                val = float(user_input)
            
            if val < 0:
                print("Error: Value cannot be negative.")
                continue
            return val
        except ValueError:
            print(f"Error: Please enter a valid {'integer' if is_int else 'number'}.")

def load_inventory():
    """Loads inventory from inventory.json and converts dictionaries into Product objects."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                raw_data = json.load(f)
            
            # Convert raw dictionaries into a list of Product objects
            inventory = []
            for item in raw_data:
                product_obj = Product(
                    product_id=item['id'], 
                    name=item['name'], 
                    price=item['price'], 
                    stock=item['stock']
                )
                inventory.append(product_obj)

            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return inventory
        except json.JSONDecodeError:
            print("Error reading inventory.json. Starting with an empty inventory.")
            return []
    else:
        print("inventory.json not found. Starting with an empty inventory.")
        return []
    


def save_inventory(inventory, silent=False):
    """Converts a list of Product objects back into dictionaries and saves to inventory.json."""
    if not silent:
        print("Saving inventory...")
    try:
        # Reconstruct the list of dictionaries using our class getter methods
        raw_data = []
        for product in inventory:
            raw_data.append({
                "id": product.get_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "stock": product.get_stock()
            })

        with open(FILENAME, "w") as f:
            json.dump(raw_data, f, indent=4)
        if not silent:
            print(f"Inventory saved successfully to {FILENAME}.")
        else:
            print("Inventory saved successfully.")
    except IOError:
        print("Error saving inventory data to file.")

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 48)

def add_product(inventory):
    print("\nAdd New Product")
    
    while True:
        prod_id = get_non_empty_input("Product ID: ")
        if any(product['id'].lower() == prod_id.lower() for product in inventory):
            print("Error: Product ID already exists. Try a different ID.")
            continue
        break

    name = get_non_empty_input("Product Name: ")
    price = get_positive_number("Price: ", is_int=False)
    stock = get_positive_number("Stock Quantity: ", is_int=True)

    new_prod = {
        "id": prod_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_prod)
    print("Product added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    prod_id = get_non_empty_input("Enter Product ID: ")
    
    for product in inventory:
        if product['id'].lower() == prod_id.lower():
            print("Product Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")
            
            new_stock = get_positive_number("New Stock Quantity: ", is_int=True)
            product['stock'] = new_stock
            print("Stock updated successfully!")
            return
            
    print("Product not found.")

def search_product(inventory):
    print("\nSearch Product")
    prod_id = get_non_empty_input("Enter Product ID: ")
    
    for product in inventory:
        if product['id'].lower() == prod_id.lower():
            print("Product Found")
            print("-" * 48)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 48)
            return
            
    print("Product not found.")

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    
    inventory = load_inventory()
    
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        
        choice = input("Enter option: ").strip()
        
        if choice == '1':
            display_all(inventory)
        elif choice == '2':
            add_product(inventory)
        elif choice == '3':
            update_stock(inventory)
        elif choice == '4':
            search_product(inventory)
        elif choice == '5':
            save_inventory(inventory)
        elif choice == '6':
            print("Saving inventory before exit...")
            save_inventory(inventory, silent=True)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        elif not choice:
            print("Error: Option cannot be empty.")
        else:
            print("Invalid option. Please choose a valid number (1-6).")

if __name__ == "__main__":
    main()
