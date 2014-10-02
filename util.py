import sys, os
from datetime import date, datetime
from decimal import *
from refreshbooks.api import *

API_DATE_FORMAT = '%Y-%m-%d 00:00:00'

def relpath(*path):
	basedir = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(basedir, *path)

def readtext(*path):
	path = relpath(*path)
	if not os.path.exists(path):
		return None

	f = open(path, 'r')
	text = f.read()
	f.close()
	return text

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

		print('...page {} of {}'.format(paged.attrib['page'], total_pages))

		page += 1

	return combined

def last_quarter(before_day):
	"get the start and end dates for the last quarter that ended before before_day"
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

def to_decimal(dec):
	if isinstance(dec, Decimal):
		return dec
	if isinstance(dec, DecimalElement): # refreshbooks.api.DecimalElement
		return dec.pyval
	return Decimal(dec)
