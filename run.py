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
        args.file, args.months, args.yearly, args.income, args.expense,
        args.add_income, args.add_expense, args.period_from, args.period_to,
        args.time, args.no_color
    )
    expenses.show()


if __name__ == '__main__':
    main(Settings())
