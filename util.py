from datetime import date, datetime
from decimal import *

API_DATE_FORMAT = '%Y-%m-%d 00:00:00'

def last_quarter(before_day):
	q_months = [1, 4, 7, 10] # months that start a quarter
	from_month = before_day.month
	end_month = max([m for m in q_months if m <= from_month])
	end_i = q_months.index(end_month)
	start_i = (end_i - 1) % len(q_months)
	start_month = q_months[start_i]
	start_year = before_day.year if end_i > start_i else before_day.year - 1
	end_year = before_day.year

	start = date(start_year, start_month, 1)
	end = date(end_year, end_month, 1)

	return (start,end)

def date_str(date):
	return date.strftime('%-d %b, %Y')

def api_date(date):
	return date.strftime(API_DATE_FORMAT)

def parse_api_date(str_el):
	return datetime.strptime(str_el.pyval, API_DATE_FORMAT).date()

def tax_amounts(invoice):
	taxable = 0
	taxes = {}

	for line in invoice.lines.line:
		if(line.tax1_name):
			taxable = taxable + line.amount.pyval
			add_tax(taxes, line.tax1_name, line.tax1_percent, line.amount.pyval)
		elif(line.tax2_name):
			taxable += line.amount.pyval
			add_tax(taxes, line.tax1_name, line.tax1_percent, line.amount.pyval)

	return taxable, taxes

def add_tax(taxes, name, percent, line_amount):
	taxes[name] = taxes.get(name, Decimal(0)) + percent / Decimal(100) * line_amount
