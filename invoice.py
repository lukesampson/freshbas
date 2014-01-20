from util import *

def paid_tax_amounts(invoice_amount, payment, taxes):
	fraction_paid = to_decimal(payment) / to_decimal(invoice_amount)

	paid = {}
	for taxname, val in taxes.items():
		taxable, tax = val
		paid[taxname] = fraction_paid * taxable, fraction_paid * tax

	return paid

def tax_amounts(invoice):
	taxes = {}

	for line in invoice.lines.line:
		amount = to_decimal(line.amount)

		if(line.tax1_name):
			add_tax(taxes, line.tax1_name, line.tax1_percent, amount)
		elif(line.tax2_name):
			add_tax(taxes, line.tax2_name, line.tax2_percent, amount)

	return taxes

def add_tax(taxes, name, percent, line_amount):
	name = str(name).upper()
	taxable, tax = taxes.get(name, (Decimal(0), Decimal(0)))

	taxable += line_amount
	tax += percent / Decimal(100) * line_amount

	taxes[name] = (taxable, tax)