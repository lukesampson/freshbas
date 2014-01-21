from util import *

def get_expenses(client, start, end):
	print('retrieving expenses...')
	res = all_pages(
		client.expense.list,
		date_from=api_date(start),
		date_to=api_date(end)
	)

	gross = 0
	untaxed = 0
	tax_totals = {}
	for expense in res.expenses.expense:
		if expense.tax1_name:
			pass

def add_taxed_expense(taxes, taxname, expense, tax):
	# note: taxamount can be less than tax % * expenseamount. For GST, we'll deal
	# with that later by treating any surplus expenseamount as untaxed
	taxname = str(taxname).upper()

	total_expenses_for_tax, tax_total = taxes.get(taxname, (Decimal(0), Decimal(0)))

	total_expenses_for_tax += expense
	tax_total += tax

	taxes[taxname] = total_expenses_for_tax, tax_total

