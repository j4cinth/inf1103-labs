"""Lab 7 tests. Run from the project folder:  python test_inventory.py"""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

import oop2_inventory_manager as app
from oop2_inventory_manager import (
    CanBeShipped, DigitalProduct, Inventory, PhysicalProduct, Product,
)


def capture(func, *args):
    """Run func and return whatever it printed."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        func(*args)
    return buf.getvalue()


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.phys = PhysicalProduct("P1", "Guitar", 499.99, 5, 3.5)
        self.dig = DigitalProduct("D1", "Photo Editor", 29.99, 100, 250.0)

    # Physical products store and display their weights
    def test_physical_stores_weight(self):
        self.assertEqual(self.phys.get_weight(), 3.5)

    def test_physical_display_has_parent_and_child_info(self):
        out = capture(self.phys.display_information)
        self.assertIn("Guitar", out)          # from Product
        self.assertIn("Weight: 3.5 kg", out)  # from PhysicalProduct

    # Digital products store and display their download sizes
    def test_digital_display_has_parent_and_child_info(self):
        out = capture(self.dig.display_information)
        self.assertIn("Photo Editor", out)
        self.assertIn("Download Size: 250.0 MB", out)

    # Both subclasses implement get_fulfilment_info()
    def test_fulfilment_info(self):
        self.assertIn("physical", self.phys.get_fulfilment_info().lower())
        self.assertIn("download", self.dig.get_fulfilment_info().lower())

    # The abstract Product class cannot be instantiated
    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("X", "Nope", 1.0, 1)

    def test_interface_is_abstract(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    # Physical products can calculate shipping costs (varies with weight)
    def test_shipping_cost_by_weight(self):
        light = PhysicalProduct("L", "Light", 10, 1, 1.0)
        heavy = PhysicalProduct("H", "Heavy", 10, 1, 10.0)
        self.assertAlmostEqual(light.calculate_shipping_cost(), 7.50)
        self.assertAlmostEqual(heavy.calculate_shipping_cost(), 30.00)
        self.assertGreater(heavy.calculate_shipping_cost(),
                           light.calculate_shipping_cost())

    # Digital products are not required to implement shipping
    def test_interface_membership(self):
        self.assertIsInstance(self.phys, CanBeShipped)
        self.assertNotIsInstance(self.dig, CanBeShipped)
        self.assertFalse(hasattr(self.dig, "calculate_shipping_cost"))

    def test_is_a_product(self):
        self.assertIsInstance(self.phys, Product)
        self.assertIsInstance(self.dig, Product)

    def test_update_stock(self):
        self.phys.update_stock(12)
        self.assertEqual(self.phys.get_stock(), 12)


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = Inventory()
        self.inv.add_product(PhysicalProduct("P1", "Guitar", 499.99, 5, 3.5))

    def test_add_and_search(self):
        self.assertEqual(self.inv.search_product("P1").get_name(), "Guitar")

    def test_search_is_case_insensitive(self):
        self.assertIsNotNone(self.inv.search_product("p1"))

    def test_search_missing_returns_none(self):
        self.assertIsNone(self.inv.search_product("nope"))

    def test_duplicate_id_rejected(self):
        dup = DigitalProduct("p1", "Dup", 1.0, 1, 1.0)
        self.assertFalse(self.inv.add_product(dup))
        self.assertEqual(len(self.inv.get_all_products()), 1)


class TestPersistence(unittest.TestCase):
    def setUp(self):
        # Point the app at a temp file so real data is never touched
        self.tmp = tempfile.TemporaryDirectory()
        self.original = app.FILENAME
        app.FILENAME = os.path.join(self.tmp.name, "inventory.json")

    def tearDown(self):
        app.FILENAME = self.original
        self.tmp.cleanup()

    def test_round_trip_preserves_types_and_attributes(self):
        inv = Inventory()
        inv.add_product(PhysicalProduct("P1", "Guitar", 499.99, 5, 3.5))
        inv.add_product(DigitalProduct("D1", "Editor", 29.99, 100, 250.0))
        capture(app.save_inventory, inv)

        with open(app.FILENAME) as f:
            types = {item["type"] for item in json.load(f)}
        self.assertEqual(types, {"physical", "digital"})

        loaded = Inventory()
        capture(app.load_inventory, loaded)
        p = loaded.search_product("P1")
        d = loaded.search_product("D1")
        self.assertIsInstance(p, PhysicalProduct)
        self.assertIsInstance(d, DigitalProduct)
        self.assertEqual(p.get_weight(), 3.5)
        self.assertEqual(p.get_stock(), 5)
        self.assertIn("Download Size: 250.0 MB", capture(d.display_information))

    def test_missing_file_starts_empty(self):
        inv = Inventory()
        capture(app.load_inventory, inv)
        self.assertEqual(inv.get_all_products(), [])

    def test_corrupt_file_does_not_crash(self):
        with open(app.FILENAME, "w") as f:
            f.write("{ not json")
        inv = Inventory()
        capture(app.load_inventory, inv)
        self.assertEqual(inv.get_all_products(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
