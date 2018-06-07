A programm for calculating average expenses from a ledger journal.

# Installation

Clone repo and maybe setup an alias to `python3 run.py`.

# Usage

To let the programm calculate your monthly / yearly expenses (and income) you can start the programm with these parameter:

	**file**		your ledger journal file. leave blank, if you set up the LEDGER_FILE variable.
	**-e**			use multiple times to add each account describing your expenses.
	**--expense**
	**-i**			same as for --expense, but for the income accounts.
	**--income**
	**-m**			define how many months should be used for the average calculation. default is 12.
	**--months**
	**-f**			won't change the account name to just the top name. default false.
	**--full-name**

# Changelog

The changelog is here [CHANGELOG.md](CHANGELOG.md).
