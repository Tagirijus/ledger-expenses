"""
A programm.

Author: Manuel Senfft (www.tagirijus.de)
"""

from general.settings import Settings
from general.expenses import Expenses


def main(settings):
    """Run the programm."""
    args = settings.args
    expenses = Expenses(
        args.file, args.full_name, args.months, args.yearly, args.income, args.expense
    )
    expenses.show()


if __name__ == '__main__':
    main(Settings())
