from refreshbooks import api
from datetime import date, timedelta
import json, income, expense, re
from util import *


config = json.loads(readtext('config.json'))
auth = config['auth']
username, token = next(iter(auth.items()))

if len(config['auth']) > 1:
	usernames = ", ".join(auth.keys())
	print("Which credential do you want to use? ({})".format(usernames))
	username = input()
	if username not in auth:
		print("No auth in config.json for {}!", username)
		exit(1)
	token = auth[username]


interactive = '-i' in sys.argv

if interactive:
	print('Which quarter do you want to report on?')
	start_year = int(input('  start year: '))
	start_month = int(input('  start month (1,4,7,10): '))
	start = date(start_year, start_month, 1)
	end = date(start_year, start_month + 3, 1)
else:
	start, end = last_quarter(date.today())

print("preparing BAS")
print("  quarter: {} - {}".format(date_str(start), date_str(end - timedelta(days=1))))

url = "{}.freshbooks.com".format(username)
client = api.TokenClient(url, token)
print("  for {}".format(username))

inc = income.get_payments(client, start, end)
exp = expense.get_expenses(client, start, end)

exp_gst_taxed_ex_gst, exp_gst, exp_gst_taxed, exp_untaxed, exp_total = exp
inc_taxable, inc_gst, inc_taxable, inc_untaxed, inc_total = inc

print("BAS WORKSHEET for {}\n".format(username))

print("G1     (total sales inc GST): ${:7.0f}".format(inc_total))

if(inc_untaxed > 0):
	print("G3    (other GST-free sales): ${:7.0f}".format(inc_untaxed))

print("G10      (capital purchases): ${:7.0f}".format(0)) # assume simple depreciation, and no expenses over $6500
print("G11  (non-capital purchases): ${:7.0f}".format(exp_total))

if(exp_untaxed > 0):
	print("G14     (GST-free purchases): ${:7.0f}".format(exp_untaxed))

print("")

inc_ex_gst = inc_total - inc_gst
exp_ex_gst = exp_total - exp_gst
print("T1 (PAYG installment income): ${:7.0f}".format(inc_ex_gst - exp_ex_gst))