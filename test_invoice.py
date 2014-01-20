from invoice import *
from decimal import *

def test_get_taxes_for_line_items():
	invoice = make_invoice([
		make_line(90.91, ('GST', 10))
	])

	gst = tax_amounts(invoice)['GST']
	assert amounts_eq(gst[0], 90.91)
	assert amounts_eq(gst[1], 9.09)

def test_get_taxes_uses_uppercase_tax_nam():
	invoice = make_invoice([
		make_line(10, ('gst', 10))
	])

	taxes = tax_amounts(invoice)
	assert 'GST' in taxes
	assert amounts_eq(taxes['GST'][1], 1)

def test_part_payment_one_tax():
	# test invoice of $1000 with $100 GST-taxable item (ignore other items)
	# payment of $205 should result in  $20.50 payment towards GST-taxable item
	invoice = make_invoice([
		make_line(90.91, ('GST', 10))
	])

	taxes = tax_amounts(invoice)
	paid = paid_tax_amounts(1000, 205, taxes)
	gst_taxable = paid['GST'][0]
	gst = paid['GST'][1]

	assert amounts_eq(20.5, gst_taxable + gst)
	assert amounts_eq(gst, gst_taxable / 10)


# helpers...

class MockObject(object):
	pass

def amounts_eq(a, b):
	return round(Decimal(a), 2) == round(Decimal(b), 2)

def make_invoice(lines):
	invoice = MockObject()
	invoice.lines = MockObject()
	invoice.lines.line = lines
	return invoice

def make_line(amount, tax1=None, tax2=None):
	line = MockObject()
	line.amount = amount
	if tax1 is not None:
		line.tax1_name = tax1[0]
		line.tax1_percent = tax1[1]

	if tax2 is not None:
		line.tax2_name = taxt[0]
		line.tax2_percent = tax2[1]

	return line
