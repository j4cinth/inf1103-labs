from oop4_inventory_manager import (
    Supplier, PhysicalProduct, Order,
    BulkDiscount, PercentageDiscount, StudentDiscount
)

# Section 2 Test
sup = Supplier("SUP-01", "Logitech Singapore", "support@logitech.sg")
item = PhysicalProduct(sup, "P001", "Test Monitor", 125.00, 10, 2.5)

order = Order("ORD-100", BulkDiscount(200, 20))
order.add_order_line(item, 2)
print(f"Total with BulkDiscount(200, 20): {order.calculate_total()}")

order.set_discount(PercentageDiscount(10))
print(f"Total with PercentageDiscount(10): {order.calculate_total()}")

order.set_discount(StudentDiscount())
print(f"Total with StudentDiscount(): {order.calculate_total()}")
