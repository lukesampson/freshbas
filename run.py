import sys, os
from lxml import objectify

dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{}/../refreshbooks".format(dir))

from refreshbooks import api
from datetime import date, timedelta
from future import standard_library
import configparser
from util import *


start, end = last_quarter(date.today())
print("BAS Quarter: {} - {}".format(date_str(start), date_str(end - timedelta(days=1))))

config = configparser.ConfigParser()
config.read('config.cfg')

c = api.TokenClient(config.get('auth', 'url'), config.get('auth', 'token'))

print('retrieving payments...')
res = c.payment.list(
	date_from=api_date(start),
	date_to=api_date(end)
)

pages = int(res.payments.attrib['pages'])

if(pages > 1):
	raise Exception("there's more than 1 page of payments! haven't handled this case!")

gross = 0
taxable = 0
gst = 0

for payment in res.payments.payment:
	invoice_id = payment.invoice_id.pyval
	invoice_res = c.invoice.get(invoice_id=invoice_id)
	invoice = invoice_res.invoice

	invoice_taxable, invoice_taxes = tax_amounts(invoice)
	fraction_paid = payment.amount.pyval / invoice.amount.pyval

	date_paid = parse_api_date(payment.date)
	print("received payment of ${} ({:.2%}) of invoice #{} (${}) on {}".format(payment.amount,
		fraction_paid, invoice.number, invoice.amount, date_paid))

	payment_taxable = invoice_taxable * fraction_paid
	payment_gst = invoice_taxes['GST'] * fraction_paid

	gross += payment.amount.pyval
	taxable += payment_taxable
	gst += payment_gst

print("collected: gross=${:.2f}, taxable=${:.2f}, GST=${:.2f}".format(gross, taxable, gst))