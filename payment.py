from util import *

def get_payments(client, start, end):
	print('retrieving payments...')
	res = all_pages(
		client.payment.list,
		date_from=api_date(start),
		date_to=api_date(end)
	)

	gross = 0
	tax_totals = {}

	for payment in res.payments.payment:
		print('${:,.2f} payment on {}'.format(to_decimal(payment.amount), date_str(parse_api_date(payment.date))))
		invoice_id = payment.invoice_id.pyval

		res = client.invoice.get(invoice_id=invoice_id)
		inv = res.invoice

		taxes = tax_amounts(inv)
		taxes_paid = paid_tax_amounts(inv.amount, payment.amount, taxes)

		# keep running total for each tax
		for taxname, val in taxes_paid.items():
			total_taxable, total_tax  = tax_totals.get(taxname, (to_decimal(0), to_decimal(0)))
			taxable, tax = val
			tax_totals[taxname] = total_taxable + taxable, total_tax + tax

		gross += payment.amount.pyval

	taxable = tax_totals['GST'][0]
	gst = tax_totals['GST'][1]

	print("INCOME:\n\tGross: ${:,.2f}, Taxable: ${:,.2f}, GST: ${:,.2f}".format(gross, taxable, gst))

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