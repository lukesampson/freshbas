from util import *

def get_expenses(client, start, end):
	print('retrieving expenses...')
	res = all_pages(
		client.expense.list,
		date_from=api_date(start),
		date_to=api_date(end)
	)

	untaxed = Decimal(0)
	taxes = {}
	for expense in res.expenses.expense:
		if expense.tax1_name:
			add_taxed_expense(taxes, expense.tax1_name, expense.amount, expense.tax1_amount)
		elif expense.tax2_name:
			add_taxed_expense(taxes, expense.tax2_name, expense.amount, expense.tax2_amount)
		else:
			untaxed += to_decimal(expense.amount)


	gst_taxed, gst = taxes['GST']
	gst_taxed_calc = gst * 11

	# handle any amount on GST-taxed expenses for which GST wasn't taxed
	surplus = gst_taxed - gst_taxed_calc
	if surplus < 0:
		# pretty sure this will never happen, I think FreshBooks won't allow it
		raise "At least one expense has more than 10%% GST!"

	untaxed += surplus
	gst_taxed_ex_gst = gst_taxed_calc - gst
	total = gst_taxed_calc + untaxed

	print("EXPENSES\n")
	print("\t Where GST was charged (ex. GST): ${:10,.2f}".format(gst_taxed_ex_gst))
	print("\t                             GST: ${:10,.2f}".format(gst))
	print("\t                                   ----------")
	print("\t          GST inclusive expenses: ${:10,.2f}".format(gst_taxed_calc))
	print("\t           Where GST not charged: ${:10,.2f}".format(untaxed))
	print("\t                                   ==========")
	print("\t                 TOTAL (inc GST): ${:10,.2f}".format(total))
	print("\t                                   ==========")

	return gst_taxed_ex_gst, gst, gst_taxed_calc, untaxed, total

def add_taxed_expense(taxes, taxname, expense, tax):
	# note: taxamount can be less than tax % * expense For GST, we'll deal
	# with that in get_expenses by treating any surplus expense as untaxed
	taxname = str(taxname).upper()

	total_expenses_for_tax, tax_total = taxes.get(taxname, (Decimal(0), Decimal(0)))

	total_expenses_for_tax += to_decimal(expense)
	tax_total += to_decimal(tax)

	taxes[taxname] = total_expenses_for_tax, tax_total

