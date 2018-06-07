import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from termcolor import colored
import os


class Expenses(object):

    def __init__(self, settings):
        self.settings = settings
        self.expense_amounts = {}
        self.income_amounts = {}

        self.ledger_command = 'ledger --collapse b {}'

    def test(self):
        """Just for testing."""
        self.getExpenseAmounts()
        print(self.settings.args)
        print(colored(self.expense_amounts, 'red'))

    def getExpenseAmounts(self):
        """Gets the amounts for all expense accounts."""
        for expense_account in self.settings.args.expense:
            expense_account_name = self.getTopAccountName(expense_account)
            self.expense_amounts[expense_account_name] = (
                self.getAmountForAccount(expense_account)
            )

    def getTopAccountName(self, account):
        """
        Gets the top account name - basically the last element of
        the :-seperated string.
        """
        if not self.settings.args.full_name:
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
        result = round(result / self.settings.args.months, 2)
        return result

    def prepareLedgerFile(self):
        """Outputs the ledger file, if given."""
        if self.settings.args.file is not None:
            return '-f {} '.format(self.settings.args.file)
        else:
            return ''

    def prepareLedgerDate(self):
        """
        Prepare the ledger date according to the months and output
        the ledger parameter.
        """
        date_to = datetime.datetime.now()
        date_to_str = date_to.strftime('%Y-%m-%d')

        date_from = date_to - relativedelta(months=self.settings.args.months)
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
