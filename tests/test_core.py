import unittest
from decimal import Decimal
from equipquote import Item, Quote

class TestQuote(unittest.TestCase):
    def test_totals_with_discount_tax_freight(self):
        q = Quote(items=[Item(name="A", quantity=2, unit_price=1000)],
                  discount_rate=0.1, tax_rate=0.13, freight=100)
        self.assertEqual(q.subtotal, Decimal("2000.00"))
        self.assertEqual(q.discount_amount, Decimal("200.00"))
        self.assertEqual(q.tax_amount, Decimal("247.00"))
        self.assertEqual(q.total, Decimal("2147.00"))

    def test_empty_items_rejected(self):
        with self.assertRaises(ValueError):
            Quote(items=[])

if __name__ == "__main__":
    unittest.main()
