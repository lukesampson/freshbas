import sys, os
from lxml import objectify

dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{}/../refreshbooks".format(dir))

from refreshbooks import api
from datetime import date, timedelta
import configparser
import util


start, end = util.last_quarter(date.today())
print("BAS Quarter: {} - {}".format(util.date_str(start), util.date_str(end - timedelta(days=1))))

config = configparser.ConfigParser()
config.read('config.cfg')

c = api.TokenClient(config.get('auth', 'url'), config.get('auth', 'token'))

res = c.invoice.list(
	date_from=util.api_date(start),
	date_to=util.api_date(end)
)

pages = int(res.invoices.attrib['pages'])

if(pages > 1):
	raise Exception("there's more than 1 page of invoices! haven't handled this case!")

print('there are {0} pages of invoice'.format(pages))

# print(objectify.dump(res))