A programm for calculating average expenses from a ledger journal.

# Installation

Clone repo and maybe setup an alias to `python3 run.py`.

# Usage

To let the programm calculate your monthly / yearly expenses (and income) you can start the programm with these parameter:

| parameter | description |
| --- | --- |
| **file** | your ledger journal file. leave blank, if you set up the LEDGER_FILE variable. |
| **-e** / **--expense** | use multiple times to add each account describing your expenses. input holds the account and its name for the ouput. |
| **-i** / **--income** | same as for --expense, but for the income accounts. |
| **-m** / **--months** | define how many months should be used for the average calculation. default is 12. |
| **-y** / **--yearly** | the programm now calculates the yearly instead of the monthly income / expenses. |

# Future

Maybe some day there will be a _python3 ledger module_ and I will embed this. The programm would be so much faster without the `os.popen` stuff.

# Changelog

The changelog is here [CHANGELOG.md](CHANGELOG.md).
