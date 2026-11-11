from oop3_inventory_manager import Supplier, PhysicalProduct, DigitalProduct, Inventory


# Test for 2.2
print("=== SECTION 2.2: TESTING ASSOCIATION ===")

sup = Supplier("SUP-01", "Logitech Singapore", "support@logitech.sg")
mouse = PhysicalProduct(sup, "P001", "MX Master 3S", 149.00, 15, 0.14)
software = DigitalProduct(sup, "D001", "Logi Options+ Pro", 29.90, 999, 85.0)

del sup
print("Deleted 'sup' variable from main script.\n")

print("--- Physical Product ---")
mouse.display_information()
print("\n--- Digital Product ---")
software.display_information()



#Test for 3.2
print("\n=== SECTION 3.2: TESTING AGGREGATION ===")

sup2 = Supplier("SUP-02", "Keychron", "sales@keychron.com")
keyboard = PhysicalProduct(sup2, "P002", "Keychron Q1 Pro", 269.00, 10, 1.7)
inv_a = Inventory()
inv_b = Inventory()

inv_a.add_product(keyboard)
print(f"In Inventory A before removal? {inv_a.find_product('P002') is not None}")
inv_a.remove_product("P002")
print(f"In Inventory A after removal? {inv_a.find_product('P002') is not None}")

print("\nProduct still works independently:")
keyboard.display_information()
inv_b.add_product(keyboard)
print(f"In Inventory B now? {inv_b.find_product('P002') is not None}")
