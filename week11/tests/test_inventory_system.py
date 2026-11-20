import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Ensure the parent directory is on the path so we can import oop4_inventory_manager
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from oop4_inventory_manager import (
    Supplier,
    Product,
    PhysicalProduct,
    DigitalProduct,
    ProductFactory,
    Inventory,
    Order,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
    get_positive_float,
    load_products,
)


class CustomFlatDiscount(DiscountStrategy):
    """Test strategy verifying Order works with new strategies without modification."""
    def apply(self, total: float) -> float:
        return max(0.0, total - 15.0)


class TestInventoryManagementSystem(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP-01", "Logitech", "support@logitech.com")
        self.physical = ProductFactory.create("physical", self.supplier, "P001", "Mouse", 100.0, 10, 0.2)
        self.digital = ProductFactory.create("digital", self.supplier, "D001", "Software", 50.0, 20, 150.0)

    # 1. Order calculates totals through DiscountStrategy
    def test_order_default_no_discount(self):
        order = Order("ORD-01")
        order.add_order_line(self.physical, 2)  # 200.0
        self.assertEqual(order.calculate_total(), 200.0)

    def test_order_bulk_and_percentage_discounts(self):
        order = Order("ORD-02", BulkDiscount(200, 20))
        order.add_order_line(self.physical, 2)
        order.add_order_line(self.digital, 1)  # Subtotal = 250.0
        self.assertEqual(order.calculate_total(), 230.0)

        # 3. Strategy on existing order can be changed with set_discount()
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

        order.set_discount(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    # 2. New discount strategy works without modifying Order
    def test_new_discount_strategy_without_changing_order(self):
        order = Order("ORD-03", CustomFlatDiscount())
        order.add_order_line(self.physical, 1)  # 100.0
        self.assertEqual(order.calculate_total(), 85.0)

    # 4 & 5. ProductFactory creates correct subclasses and rejects unknown types
    def test_product_factory_creation_and_unknown_type(self):
        self.assertIsInstance(self.physical, PhysicalProduct)
        self.assertIsInstance(self.physical, Product)
        self.assertIsInstance(self.digital, DigitalProduct)
        self.assertIsInstance(self.digital, Product)

        with self.assertRaises(ValueError):
            ProductFactory.create("service", self.supplier, "S001", "Install", 30.0, 5)

    # 6. Invalid prices, stock quantities, and order quantities are rejected
    def test_validation_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", self.supplier, "P002", "BadPrice", 0.0, 5)
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", self.supplier, "P003", "NegPrice", -10.0, 5)
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", self.supplier, "D002", "NegStock", 20.0, -1)
        with self.assertRaises(ValueError):
            self.physical.update_stock(-5)

        order = Order("ORD-04")
        with self.assertRaises(ValueError):
            order.add_order_line(self.physical, 0)
        with self.assertRaises(ValueError):
            order.add_order_line(self.physical, -2)

    # 7. Invalid user input is handled gracefully and re-prompted
    @patch("builtins.input", side_effect=["abc", "-5", "0", "12.50"])
    def test_get_positive_float_reprompts_until_valid(self, mock_input):
        result = get_positive_float("Enter price: ")
        self.assertEqual(result, 12.50)
        self.assertEqual(mock_input.call_count, 4)

    # 8 & 9. Missing CSV handled gracefully; bad CSV rows skipped while valid rows load
    def test_load_products_missing_file(self):
        inv = Inventory()
        # Should not raise FileNotFoundError
        load_products("non_existent_file.csv", inv, self.supplier)
        self.assertEqual(len(inv.get_all_products()), 0)

    def test_load_products_skips_bad_rows_and_loads_valid_rows(self):
        csv_content = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, newline="") as tmp:
            tmp.write(csv_content)
            tmp_path = tmp.name

        try:
            inv = Inventory()
            load_products(tmp_path, inv, self.supplier)
            loaded_ids = [p.get_id() for p in inv.get_all_products()]
            self.assertEqual(loaded_ids, ["P001", "D001", "P003"])
        finally:
            os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
