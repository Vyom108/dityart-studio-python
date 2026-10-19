"""Catalog filtering and WhatsApp link checks."""

import json
import unittest
from pathlib import Path

from storefront import filter_products, whatsapp_link


class StorefrontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).parents[1]
        items = json.loads((root / "data" / "products.json").read_text(encoding="utf-8"))
        labels = {"personalized-gifts": "Personalized Gifts", "kids-stationery": "Kids Stationery", "corporate-branding": "Corporate Branding"}
        cls.products = [{**item, "category_label": labels[item["category"]]} for item in items]

    def test_category_and_search_filters_can_be_combined(self):
        matches = filter_products(self.products, "Kids Stationery", "coloring")
        self.assertEqual([item["name"] for item in matches], ["Coloring Books"])
        self.assertEqual(len(filter_products(self.products, "Corporate Branding")), 6)
        self.assertEqual(filter_products(self.products, "All categories", "no such item"), [])

    def test_whatsapp_link_encodes_prefilled_product_message(self):
        link = whatsapp_link("Hi! Tell me about Wallet Cards")
        self.assertTrue(link.startswith("https://wa.me/919081913600?text="))
        self.assertIn("Wallet%20Cards", link)
        self.assertNotIn(" ", link)


if __name__ == "__main__":
    unittest.main()
