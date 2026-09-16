# Week 2, Lab 2

# 1. Initialize variables
total_inventory = 0
failed_entries = 0

# 2. Continuous loop until user types 'quit'
while True:
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()
    
    # Check if user wants to quit
    if user_input.lower() == 'quit':
        break
          
    # 4. Handle invalid input: Check if it's a positive digit
    if not user_input.isdigit():
        print("Error: Invalid entry. Please enter a valid integer.")
        failed_entries += 1
        continue  # Move to the next iteration
        
    # Convert string to integer
    stock_value = int(user_input)
    
    # 5. Enforce business rules: Reject negative numbers
    if stock_value < 0:
        print("Error: Negative values are not allowed.")
        failed_entries += 1
        continue