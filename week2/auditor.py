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
          
