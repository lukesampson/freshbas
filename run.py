import sys, os
from lxml import objectify

dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append("{}/../refreshbooks".format(dir))

from refreshbooks import api
from datetime import datetime
import configparser

#start = datetime.now()
#print(start)

config = configparser.ConfigParser()
config.read('config.cfg')

c = api.TokenClient(config.get('auth', 'url'), config.get('auth', 'token'))

invoices_response = c.invoice.list()

print(objectify.dump(invoices_response))