import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
import os
from tabulate import tabulate
from termcolor import colored


class Expenses(object):

    def __init__(
        self,
        ledger_file=None,
        full_name=False,
        months=12,
        yearly=False,
        income_accounts=[],
        expense_accounts=[]
    ):
        self.ledger_file = ledger_file
        self.full_name = full_name
        self.months = months
        self.yearly = yearly

        self.income_accounts = income_accounts
        self.expense_accounts = expense_accounts
        self.income_amounts = {}
        self.expense_amounts = {}
        self.getAmounts()

    def show(self):
        """Output the main results."""
        self.printAmounts('Income accounts', self.income_amounts, 'blue')
        print()
        self.printAmounts('Expense accounts', self.expense_amounts, 'yellow')

    def printAmounts(self, title, amounts_dict, color):
        """Print an amounts dict as a table."""
        print(
            tabulate(
                self.prepareTable(amounts_dict, color),
                headers=[colored(title, 'white'), colored('€', 'white')],
                tablefmt='plain'
            )
        )

    def prepareTable(self, amounts_dict, color):
        """Prepare the table according to the given amounts_dict."""
        output = []
        for account in amounts_dict:
            acc_str = colored(account, color)
            amount = self.colorAmount(amounts_dict[account])
            output += [[acc_str, amount]]
        return output

    def colorAmount(self, amount):
        """Depending on negative or positive, color the amount."""
        if amount > 0:
            return colored(str(amount), 'green')
        else:
            return colored(str(amount), 'red')

    def getAmounts(self):
        """Get income and expenses amounts."""
        self.getIncomeAmounts()
        self.getExpenseAmounts()

    def getIncomeAmounts(self):
        """Gets the amounts for all income accounts."""
        for income_account in self.income_accounts:
            income_account_name = self.getTopAccountName(income_account)
            self.income_amounts[income_account_name] = (
                self.getAmountForAccount(income_account)
            )

    def getExpenseAmounts(self):
        """Gets the amounts for all expense accounts."""
        for expense_account in self.expense_accounts:
            expense_account_name = self.getTopAccountName(expense_account)
            self.expense_amounts[expense_account_name] = (
                self.getAmountForAccount(expense_account)
            )

    def getTopAccountName(self, account):
        """
        Gets the top account name - basically the last element of
        the :-seperated string.
        """
        if not self.full_name:
            seperated = str(account).split(':')
            return seperated[-1]
        else:
            return account

    def getAmountForAccount(self, account):
        """Gets the amount of the given account."""
        ledger_file = self.prepareLedgerFile()
        ledger_date = self.prepareLedgerDate()
        ledger_command = 'ledger {}{} --collapse b {}'.format(
            ledger_file, ledger_date, account
        )
        result = self.prepareAmount(os.popen(ledger_command).readline().strip())
        if self.yearly:
            result = round((result / self.months) * 12, 2) * -1
        else:
            result = round(result / self.months, 2) * -1
        return result

    def prepareLedgerFile(self):
        """Outputs the ledger file, if given."""
        if self.ledger_file is not None:
            return '-f {} '.format(self.ledger_file)
        else:
            return ''

    def prepareLedgerDate(self):
        """
        Prepare the ledger date according to the months and output
        the ledger parameter.
        """
        date_to = datetime.datetime.now()
        date_to_str = date_to.strftime('%Y-%m-%d')

        date_from = date_to - relativedelta(months=self.months)
        date_from_str = date_from.strftime('%Y-%m-%d')

        return '-p "from {} to {}"'.format(date_from_str, date_to_str)

    def prepareAmount(self, amount_str):
        """Convert the given ledger output amount string to a decimal."""
        try:
            amount_str = amount_str[2:]
            amount_str = amount_str[:amount_str.find(' ')]
            amount_str = amount_str.replace('.', '').replace(',', '.')
            return Decimal(amount_str)
        except Exception:
            return Decimal(0)
