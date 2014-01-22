# Method of preparing BAS

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


### Assumptions

For this to work for you, the following assumptions must be true:

* You account for GST on a [cash basis](http://www.ato.gov.au/Business/Small-business-entity-concessions/In-detail/GST/Cash-and-non-cash-accounting/)
* You don't record any other taxes on invoices or expenses besides GST
* You use the [simplified depreciation rules](http://www.ato.gov.au/business/small-business-entity-concessions/in-detail/income-tax/simplified-depreciation-rules/) (depreciating assets under $6500 can be written off immediately), and all expenses recorded in FreshBooks are $6500 or less.