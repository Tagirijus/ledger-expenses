"""
A programm.

Author: Manuel Senfft (www.tagirijus.de)
"""

from general.settings import Settings
from general.expenses import Expenses


def main(settings):
    """Run the programm."""
    expenses = Expenses(settings)
    expenses.test()


if __name__ == '__main__':
    main(Settings())
