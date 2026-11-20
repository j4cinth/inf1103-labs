import os
from oop4_inventory_manager import (
    Supplier, PhysicalProduct, Order,
    BulkDiscount, PercentageDiscount, StudentDiscount,
    ProductFactory, Inventory, get_positive_float, load_products
)

# Section 2 Test
print("\n=== TESTING SECTION 2 ===")
sup = Supplier("SUP-01", "Logitech Singapore", "support@logitech.sg")
item = PhysicalProduct(sup, "P001", "Test Monitor", 125.00, 10, 2.5)

order = Order("ORD-100", BulkDiscount(200, 20))
order.add_order_line(item, 2)
print(f"Total with BulkDiscount(200, 20): {order.calculate_total()}")

order.set_discount(PercentageDiscount(10))
print(f"Total with PercentageDiscount(10): {order.calculate_total()}")

order.set_discount(StudentDiscount())
print(f"Total with StudentDiscount(): {order.calculate_total()}")

# Section 3 Test
print("\n=== TESTING SECTION 3 ===")
p1 = ProductFactory.create("physical", sup, "P002", "Keyboard", 99.0, 5, 1.2)
p2 = ProductFactory.create("digital", sup, "D001", "Antivirus", 39.0, 50, 120.0)
print(f"Created via factory: {type(p1).__name__}, {type(p2).__name__}")

try:
    ProductFactory.create("service", sup, "S001", "Setup", 30.0, 5)
except ValueError as e:
    print(f"Caught expected error: {e}")

# Section 4 Test
print("\n=== TESTING SECTION 4 ===")
for label, fn in [
    ("Zero price", lambda: ProductFactory.create("physical", sup, "P99", "Bad", 0, 5)),
    ("Negative stock", lambda: ProductFactory.create("digital", sup, "D99", "Bad", 10.0, -1)),
    ("Zero order qty", lambda: order.add_order_line(item, 0)),
]:
    try:
        fn()
    except ValueError as e:
        print(f"Validation passed ({label}): {e}")

# Section 5.1 Test
print("\n=== TESTING SECTION 5.1 ===")
val = get_positive_float("Enter positive price (test abc, -5, 12.50): ")
print(f"Returned value: {val}")

# Section 5.2 Test
print("\n=== TESTING SECTION 5.2 ===")
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv")
csv_inv = Inventory()
load_products(csv_path, csv_inv, sup)

print("\n--- Testing missing CSV file ---")
load_products("missing_products.csv", csv_inv, sup)