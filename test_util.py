from datetime import date, datetime
import util

def test_last_quarter():
	assert util.last_quarter(date(2014,1,11)) == (date(2013,10,1), date(2014,1,1))
	assert util.last_quarter(date(2014,1,1)) == (date(2013,10,1), date(2014,1,1))
	assert util.last_quarter(date(2014,6,30)) == (date(2014,1,1), date(2014,4,1))
	assert util.last_quarter(date(2014,7,1)) == (date(2014,4,1), date(2014,7,1))
	assert util.last_quarter(date(2014,9,30)) == (date(2014,4,1), date(2014,7,1))
	assert util.last_quarter(date(2014,10,1)) == (date(2014,7,1), date(2014,10,1))
	assert util.last_quarter(date(2014,12,30)) == (date(2014,7,1), date(2014,10,1))