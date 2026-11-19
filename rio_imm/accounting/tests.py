from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock
from django.test import SimpleTestCase
from .models import Invoice


class InvoiceDiscountTaxTests(SimpleTestCase):
    def test_discount_reduces_taxable_fees_first(self):
        cases = [
            ([("100", True), ("200", False)], "50", "6.50", "256.50"),
            ([("100", True), ("200", False)], "100", "0", "200"),
            ([("100", True)], "50", "6.50", "56.50"),
            ([("100", True), ("100", False)], "50", "6.50", "156.50"),
            ([("100", True)], "0", "13", "113"),
            ([("100", True)], "-50", "13", "113"),
            ([("100", True)], "150", "0", "0"),
            ([("100", False)], "50", "0", "50"),
        ]
        for amounts, discount, tax, total in cases:
            with self.subTest(amounts=amounts, discount=discount):
                invoice = SimpleNamespace(items=Mock(), save=Mock(),
                    discount_amount=Decimal(discount), tax_rate=Decimal("13"))
                invoice.items.all.return_value = [
                    SimpleNamespace(line_total=Decimal(amount), is_taxable=taxable)
                    for amount, taxable in amounts
                ]
                Invoice.calculate_totals(invoice)
                self.assertEqual(invoice.tax_amount, Decimal(tax))
                self.assertEqual(invoice.total_amount, Decimal(total))
                invoice.save.assert_called_once_with()
