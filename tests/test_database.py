"""Basic validation and SQLite persistence checks."""

import tempfile
import unittest
from pathlib import Path

from database import get_connection, save_order, validate_order


class OrderDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "orders.sqlite3"
        self.order = {
            "customer_name": "Asha Patel", "phone": "+91 90819 13600",
            "email": "asha@example.com", "city": "Rajkot", "product": "Wallet Cards",
            "category": "Personalized Gifts", "recipient_name": "Ravi", "required_text": "Happy birthday!",
            "occasion": "Birthday", "budget": "₹1,000", "preferred_colours": "Yellow",
            "required_date": "2026-11-01", "notes": "Add a photo",
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_order_is_saved_privately_with_new_status(self):
        order_id = save_order(self.order, self.db)
        with get_connection(self.db) as connection:
            row = connection.execute("SELECT * FROM custom_orders WHERE id = ?", (order_id,)).fetchone()
        self.assertEqual(row["customer_name"], "Asha Patel")
        self.assertEqual(row["status"], "New")
        self.assertEqual(row["preferred_colours"], "Yellow")
        self.assertEqual(row["recipient_name"], "Ravi")
        self.assertEqual(row["required_text"], "Happy birthday!")

    def test_required_fields_and_email_are_validated(self):
        self.assertEqual(validate_order(self.order), [])
        invalid = {**self.order, "customer_name": "", "phone": "abc", "email": "not-an-email"}
        errors = validate_order(invalid)
        self.assertTrue(any("Name is required" in error for error in errors))
        self.assertTrue(any("valid phone" in error for error in errors))
        self.assertTrue(any("valid email" in error for error in errors))

    def test_missing_required_data_does_not_create_a_row(self):
        with self.assertRaises(ValueError):
            save_order({"customer_name": "", "phone": "", "city": "", "product": ""}, self.db)
        with get_connection(self.db) as connection:
            count = connection.execute("SELECT COUNT(*) FROM custom_orders").fetchone()[0]
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
