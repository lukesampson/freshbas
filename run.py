from refreshbooks import api
from datetime import date, timedelta
import configparser, income, expense
from util import *


config = configparser.ConfigParser()
config.read('config.cfg')

start, end = last_quarter(date.today())
print("BAS Quarter: {} - {}".format(date_str(start), date_str(end - timedelta(days=1))))

client = api.TokenClient(config.get('auth', 'url'), config.get('auth', 'token'))

inc = income.get_payments(client, start, end)
exp = expense.get_expenses(client, start, end)

exp_gst_taxed_ex_gst, exp_gst, exp_gst_taxed, exp_untaxed, exp_total = exp
inc_taxable, inc_gst, inc_taxable, inc_untaxed, inc_total = inc

print("BAS WORKSHEET\n")

print(" G1: ${:7.0f}".format(inc_total))

if(inc_untaxed > 0):
	print("G3: ${:7.0f}".format(inc_untaxed))

print("G10: ${:7.0f}".format(0)) # assume simple depreciation, and no expenses over $6500
print("G11: ${:7.0f}".format(exp_total))

if(exp_untaxed > 0):
	print("G14: ${:7.0f}".format(exp_untaxed))

print("")

inc_ex_gst = inc_total - inc_gst
exp_ex_gst = exp_total - exp_gst
print(" T1: ${:7.0f}".format(inc_ex_gst - exp_ex_gst))