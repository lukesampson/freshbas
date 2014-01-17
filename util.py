from datetime import date

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
	return date.strftime('%Y-%m-%d 00:00:00')