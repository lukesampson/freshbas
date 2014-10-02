# FreshBAS
This program downloads your accounting data from FreshBooks for the last financial quarter, and prints out a table
of values which you can easily enter into your BAS worksheet, e.g.:

```text
BAS WORKSHEET

 G1: $  48000
G10: $      0
G11: $  22496
G14: $    494

 T1: $  23140
```

*Disclaimer: I'm not an accountant, and I can't guarantee that this program will give you valid data!*

### Instructions

###### Prerequisites:

* Python 3
* [refreshbooks](https://pypi.python.org/pypi/refreshbooks) package (`pip install refreshbooks`)

###### Setup:

* Copy config.json.example to confg.json, and fill in your FreshBooks username and token.

###### Running:

`python3 run.py`
This will report on the last quarter that ended before today's date.

`python3 run.py -i`
Run in interactive mode, allowing you to specify which quarter you want to report on.

### Assumptions

For this to work for you, the following assumptions must be true:

* You calculate and report GST quarterly
* You account for GST on a [cash basis](http://www.ato.gov.au/Business/Small-business-entity-concessions/In-detail/GST/Cash-and-non-cash-accounting/)
* You don't record any other taxes on invoices or expenses besides GST
* You use the [simplified depreciation rules](http://www.ato.gov.au/business/small-business-entity-concessions/in-detail/income-tax/simplified-depreciation-rules/) (depreciating assets under $6500 can be written off immediately), and all expenses recorded in FreshBooks are $6500 or less.
* You don't record non-deductible expenses in FreshBooks


### Method of preparing BAS manually through FreshBooks

Prep: make sure all received invoices have been marked as expenses.

Reports > Tax Summary:
 -- make sure dates are exact (especially if an invoice has just been paid)
 -- make sure revenue is: Collected (Cash based)
 
 (G1) Use Gross Collected
 (1A) Use G1 / 11
 (1B) Use tax on expenses

Expenses: go to Reports > Profit and loss
 -- change expenses to "Include Sales Tax"
 -- make sure it's cash based

 (G11) Use total expenses 
 
 * Simple depreciation rules mean capital purchases under $1000 can go under non-capital purchases (G11)

PAYG income = (G1) - (1A) - (G11) + (1B)

* If it's negative, just enter 0. You might record it to offset the next quarter's income, but if it's the final quarter don't worry—it'll be adjusted for in the income tax