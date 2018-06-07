A programm for calculating average expenses from a ledger journal.

# Installation

Clone repo and maybe setup an alias to `python3 run.py`.

# Usage

To let the programm calculate your monthly / yearly expenses (and income) you can start the programm with these parameter:

| command | description |
| --- | --- |
| **file** | your ledger journal file. leave blank, if you set up the LEDGER_FILE variable. |
| **-e** / **--expense** | use multiple times to add each account describing your expenses. |
| **-i** / **--income** | same as for --expense, but for the income accounts. |
| **-m** / **--months** | define how many months should be used for the average calculation. default is 12. |
| **-f** / **--full-name** | won't change the account name to just the top name. default false. |

# Changelog

The changelog is here [CHANGELOG.md](CHANGELOG.md).
