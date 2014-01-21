from refreshbooks import api
from datetime import date, timedelta
import configparser, payment, expense
from util import *


config = configparser.ConfigParser()
config.read('config.cfg')

start, end = last_quarter(date.today())
print("BAS Quarter: {} - {}".format(date_str(start), date_str(end - timedelta(days=1))))

client = api.TokenClient(config.get('auth', 'url'), config.get('auth', 'token'))

payment.get_payments(client, start, end)
expense.get_expenses(client, start, end)