from oop3_inventory_manager import Supplier, PhysicalProduct, DigitalProduct

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
