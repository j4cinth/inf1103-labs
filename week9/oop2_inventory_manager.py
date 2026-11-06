import os
import json

FILENAME = "inventory.json"

from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """Interface-style abstract base class specifying shipping capability."""
    
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Computes the shipping fees based on implementation rules."""
        pass

class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_id(self): return self.__product_id
    def get_name(self): return self.__name
    def get_price(self): return self.__price
    def get_stock(self): return self.__stock

    def update_stock(self, quantity: int):
        self.__stock  = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # Abstract method required by all subclasses
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Returns a message explaining how the product is delivered."""
        pass

    def to_dict(self) -> dict:
        return {"id": self.__product_id, "name": self.__name,
            "price": self.__price, "stock": self.__stock}


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        # Reuse parent constructor
        super().__init__(product_id, name, price, stock)
        self.__weight  = weight  # Weight in kg
    
    def get_weight(self): return self.__weight

    # Method Overriding: Reuse parent view and add unique attribute
    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight } kg")

    # Concrete implementation of abstract method
    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping handling."

    # Concrete implementation of interface contract
    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.__weight  * 2.50)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        # Reuse parent constructor
        super().__init__(product_id, name, price, stock)
        self.__download_size  = download_size  # Size in MB

    # Method Overriding: Reuse parent view and add unique attribute
    def display_information(self):
        super().display_information()
        print(f"Type: Digital | Download Size: {self.__download_size } MB")

    # Concrete implementation of abstract method
    def get_fulfilment_info(self) -> str:
        return "Delivered instantly via virtual download link."
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

class Inventory:
    """Manages a collection of Product objects."""
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Adds a product if the ID doesn't already exist."""
        for p in self.__products:
            if p.get_id().lower() == product.get_id().lower():   
                return False
        self.__products.append(product)
        return True

    def get_all_products(self):
        """Returns the list of products."""
        return self.__products

    def search_product(self, product_id):
        """Searches for a product by ID."""
        for product in self.__products:
            if product.get_id().lower() == product_id.lower():   
                return product
        return None

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

def load_inventory(inventory_obj: Inventory):
    """Loads inventory from inventory.json and converts dictionaries into correct Product subclasses."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as f:
                raw_data = json.load(f)
            
            for item in raw_data:
                product_type = item.get('type') 
                
                if product_type == "physical":
                    product_obj = PhysicalProduct(
                        product_id=item['id'], 
                        name=item['name'], 
                        price=item['price'], 
                        stock=item['stock'],
                        weight=item['weight']
                    )
                elif product_type == "digital":
                    product_obj = DigitalProduct(
                        product_id=item['id'], 
                        name=item['name'], 
                        price=item['price'], 
                        stock=item['stock'],
                        download_size=item['download_size']
                    )
                else:
                    continue # Skip unrecognized types
                
                inventory_obj.add_product(product_obj)

            print("inventory.json found.")
            print("Inventory loaded successfully.")
        except (json.JSONDecodeError, KeyError):
            print("Error reading inventory.json. Starting with an empty inventory.")
    else:
        print("inventory.json not found. Starting with an empty inventory.")

def save_inventory(inventory_obj: Inventory, silent=False):
    """Converts Product subclass objects using their to_dict methods and saves to inventory.json."""
    if not silent:
        print("Saving inventory...")
    try:
        raw_data = []
        for product in inventory_obj.get_all_products():
            # Dynamically fetch the correct structural dictionary from the child class
            raw_data.append(product.to_dict())

        with open(FILENAME, "w") as f:
            json.dump(raw_data, f, indent=4)
        if not silent:
            print(f"Inventory saved successfully to {FILENAME}.")
        else:
            print("Inventory saved successfully.")
    except IOError:
        print("Error saving inventory data to file.")

def display_all(inventory_obj: Inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    products = inventory_obj.get_all_products()
    if not products:
        print("No products in inventory.")
    for product in products:
        product.display_information()
    print("-" * 48)

def add_product_ui(inventory_obj: Inventory):
    print("\nAdd New Product")
    
    # Prompt user to choose product type
    while True:
        product_type = get_non_empty_input("Enter product type (physical/digital): ").strip().lower()
        if product_type in ["physical", "digital"]:
            break
        print("Error: Invalid type. Please enter 'physical' or 'digital'.")

    while True:
        prod_id = get_non_empty_input("Product ID: ")
        if inventory_obj.search_product(prod_id) is not None:
            print("Error: Product ID already exists. Try a different ID.")
            continue
        break

    name = get_non_empty_input("Product Name: ")
    price = get_positive_number("Price: ", is_int=False)
    stock = get_positive_number("Stock Quantity: ", is_int=True)

    # Gather specialized type attributes based on selection
    if product_type == "physical":
        weight = get_positive_number("Weight (kg): ", is_int=False)
        new_prod = PhysicalProduct(prod_id, name, price, stock, weight)
    else:
        download_size = get_positive_number("Download Size (MB): ", is_int=False)
        new_prod = DigitalProduct(prod_id, name, price, stock, download_size)

    inventory_obj.add_product(new_prod)
    print(f"{product_type.capitalize()} product added successfully!")

def update_stock_ui(inventory_obj: Inventory):
    print("\nUpdate Stock")
    prod_id = get_non_empty_input("Enter Product ID: ")
    
    product = inventory_obj.search_product(prod_id)
    if product:
        print("Product Found:")
        print(f"Name: {product.get_name()}")
        print(f"Current Stock: {product.get_stock()}")
        
        new_stock = get_positive_number("New Stock Quantity: ", is_int=True)
        product.update_stock(new_stock)
        print("Stock updated successfully!")
    else:
        print("Product not found.")

def search_product_ui(inventory_obj: Inventory):
    print("\nSearch Product")
    prod_id = get_non_empty_input("Enter Product ID: ")
    
    product = inventory_obj.search_product(prod_id)
    if product:
        print("Product Found")
        print("-" * 48)
        product.display_information()
        print(f"Fulfilment: {product.get_fulfilment_info()}")
        
        # Check if the product implements the interface
        if isinstance(product, CanBeShipped):
            print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        print("-" * 48)
    else:
        print("Product not found.")

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    
    # Corrected: Create the object and pass it to the loader function
    inventory = Inventory()
    load_inventory(inventory)
    
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
        
        # Corrected: Pointed all choices to their respective UI functions
        if choice == '1':
            display_all(inventory)
        elif choice == '2':
            add_product_ui(inventory)
        elif choice == '3':
            update_stock_ui(inventory)
        elif choice == '4':
            search_product_ui(inventory)
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
