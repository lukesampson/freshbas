from util import *
add_refreshbooks_path()

from lxml import objectify
from refreshbooks import api

from datetime import date, timedelta
from future import standard_library
import configparser
from invoice import *
from util import *
import inspect

def all_pages(api_fn, *args, **kwargs):
	"simplifies getting all pages for API functions that use pagination"

	kwargs['per_page'] = 100 # max allowed by FreshBooks API
	page = 1
	combined = None
	total = 0
	total_pages = None
	while total_pages is None or page <= total_pages:
		kwargs['page'] = page
		res = api_fn(*args, **kwargs)
		
		paged = res.find('*[1]') # get first child of root

		if combined is None:
			total = int(paged.attrib['total'])
			total_pages = int(paged.attrib['pages'])
			combined = res
		else:
			original_page = combined.find('*[1]')
			for el in paged.find('*'):
				original_page.append(el)

		print('got page {} of {}'.format(paged.attrib['page'], total_pages))

		page += 1

	return combined

def get_payments(c, start, end):
	print('retrieving payments...')
	res = all_pages(
		c.payment.list,
		date_from=api_date(start),
		date_to=api_date(end)
	)

	pages = int(res.payments.attrib['pages'])

	if(pages > 1):
		raise Exception("there's more than 1 page of payments! haven't handled this case!")

	gross = 0
	tax_totals = {}

	for payment in res.payments.payment:
		print('${:,.2f} payment on {}'.format(to_decimal(payment.amount), date_str(parse_api_date(payment.date))))
		invoice_id = payment.invoice_id.pyval

		invoice_res = c.invoice.get(invoice_id=invoice_id)
		invoice = invoice_res.invoice

		taxes = tax_amounts(invoice)
		taxes_paid = paid_tax_amounts(invoice.amount, payment.amount, taxes)

		# keep running total for each tax
		for taxname, val in taxes_paid.items():
			total_taxable, total_tax  = tax_totals.get(taxname, (to_decimal(0), to_decimal(0)))
			taxable, tax = val
			tax_totals[taxname] = total_taxable + taxable, total_tax + tax

		gross += payment.amount.pyval

	taxable = tax_totals['GST'][0]
	gst = tax_totals['GST'][1]

	print("INCOME:\n\tGross: ${:,.2f}, Taxable: ${:,.2f}, GST: ${:,.2f}".format(gross, taxable, gst))

start, end = last_quarter(date.today())
print("BAS Quarter: {} - {}".format(date_str(start), date_str(end - timedelta(days=1))))

config = configparser.ConfigParser()
config.read('config.cfg')

c = api.TokenClient(config.get('auth', 'url'), config.get('auth', 'token'))

get_payments(c, start, end)

# expenses
print('retrieving expenses...')

x = all_pages(
	c.expense.list,
	date_from=api_date(start),
	date_to=api_date(end)
)

print(x.find('*[1]').countchildren())
#pages = int(res.expenses.attrib['pages'])
#print("there are {} pages of expenses".format(pages))