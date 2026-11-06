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
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity: int):
        self.stock = quantity

    def display_information(self):
        print(f"ID: {self.product_id} | Name: {self.name} | Price: ${self.price:.2f} | Stock: {self.stock}")

    # Abstract method required by all subclasses
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Returns a message explaining how the product is delivered."""
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, weight: float):
        # Reuse parent constructor
        super().__init__(product_id, name, price, stock)
        self.weight = weight  # Weight in kg

    # Method Overriding: Reuse parent view and add unique attribute
    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.weight} kg")

    # Concrete implementation of abstract method
    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping handling."

    # Concrete implementation of interface contract
    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.weight * 2.50)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "weight": self.weight
        }

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, download_size: float):
        # Reuse parent constructor
        super().__init__(product_id, name, price, stock)
        self.download_size = download_size  # Size in MB

    # Method Overriding: Reuse parent view and add unique attribute
    def display_information(self):
        super().display_information()
        print(f"Type: Digital | Download Size: {self.download_size} MB")

    # Concrete implementation of abstract method
    def get_fulfilment_info(self) -> str:
        return "Delivered instantly via virtual download link."
    
    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "download_size": self.download_size
        }

class Inventory:
    """Manages a collection of Product objects."""
    def __init__(self):
        self.__products = []

    def add_product(self, product: Product) -> bool:
        """Adds a product if the ID doesn't already exist."""
        for p in self.__products:
            if p.product_id.lower() == product.product_id.lower():
                return False
        self.__products.append(product)
        return True

    def get_all_products(self):
        """Returns the list of products."""
        return self.__products

    def search_product(self, product_id: str) -> Product:
        """Searches for a product by ID."""
        for product in self.__products:
            if product.product_id.lower() == product_id.lower():
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
                product_type = item.get('type', 'physical') # Defaults to physical if not present
                
                if product_type == "physical":
                    product_obj = PhysicalProduct(
                        product_id=item['id'], 
                        name=item['name'], 
                        price=item['price'], 
                        stock=item['stock'],
                        weight=item.get('weight', 0.0)
                    )
                elif product_type == "digital":
                    product_obj = DigitalProduct(
                        product_id=item['id'], 
                        name=item['name'], 
                        price=item['price'], 
                        stock=item['stock'],
                        download_size=item.get('download_size', 0.0)
                    )
                else:
                    continue # Skip unrecognized types
                
                inventory_obj.add_product(product_obj)

            print("inventory.json found.")
            print("Inventory loaded successfully.")
        except json.JSONDecodeError:
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
    
    while True:
        prod_id = get_non_empty_input("Product ID: ")
        if inventory_obj.search_product(prod_id) is not None:
            print("Error: Product ID already exists. Try a different ID.")
            continue
        break

    name = get_non_empty_input("Product Name: ")
    price = get_positive_number("Price: ", is_int=False)
    stock = get_positive_number("Stock Quantity: ", is_int=True)

    new_prod = Product(prod_id, name, price, stock)
    inventory_obj.add_product(new_prod)
    print("Product added successfully!")

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
        print(f"ID: {product.get_id()}")
        print(f"Name: {product.get_name()}")
        print(f"Price: ${product.get_price():.2f}")
        print(f"Stock: {product.get_stock()}")
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
