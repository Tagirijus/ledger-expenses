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
        months=12,
        yearly=False,
        income_accounts=[],
        expense_accounts=[],
        add_income_accounts=[],
        add_expense_accounts=[]
    ):
        self.ledger_file = ledger_file
        self.months = months
        self.yearly = yearly

        self.income_accounts, self.income_accounts_name = (
            self.interpreteAccounts(income_accounts)
        )
        self.expense_accounts, self.expense_accounts_name = (
            self.interpreteAccounts(expense_accounts)
        )
        null, self.add_income_accounts = (
            self.interpreteAccounts(add_income_accounts)
        )
        null, self.add_expense_accounts = (
            self.interpreteAccounts(add_expense_accounts)
        )
        self.income_amounts = {}
        self.expense_amounts = {}
        self.getAmounts()

    def interpreteAccounts(self, accounts):
        """
        Returns a tuple with first value is a list of all account ledger-names
        and the second is a dict with all the account ledger-names as keys
        and the caption name as value.
        """
        acc = []
        name = {}
        for account in accounts:
            acc += [account[0]]
            name[account[0]] = account[1]
        return (acc, name)

    def show(self, color='white'):
        """Output the main results."""
        if self.yearly:
            what = colored('Average yearly income / expenses based on', color)
        else:
            what = colored('Average monthly income / expenses based on', color)
        months = '{} {}'.format(
            colored(self.months, color, attrs=['bold']),
            colored('months', color)
        )
        print()
        print(colored('{} {}'.format(what, months), color))
        print()
        self.printAmounts('Income accounts', self.income_amounts, 'blue', color)
        print()
        self.printAmounts('Expense accounts', self.expense_amounts, 'yellow', color)
        print()
        print()
        self.printBoth(color)
        print()

    def printBoth(self, gui_color='white'):
        """Print the income versus the expenses."""
        income_total = sum(self.income_amounts.values())
        expense_total = sum(self.expense_amounts.values())
        total = income_total + expense_total
        print('{} {}'.format(
            colored('Total money flow:', gui_color),
            self.colorAmount(total)
        ))

    def printAmounts(self, title, amounts_dict, color, gui_color='white'):
        """Print an amounts dict as a table."""
        print(
            tabulate(
                self.prepareTable(amounts_dict, color),
                headers=[colored(title, gui_color), colored('€', gui_color)],
                tablefmt='plain'
            )
        )

    def prepareTable(self, amounts_dict, color):
        """Prepare the table according to the given amounts_dict."""
        output = []
        for account in sorted(amounts_dict):
            acc_str = colored(account, color)
            amount = self.colorAmount(amounts_dict[account])
            output += [[acc_str, amount]]
        output += [[
            colored('--- Total', color),
            self.colorAmount(sum(amounts_dict.values()))
        ]]
        return output

    def colorAmount(self, amount):
        """Depending on negative or positive, color the amount."""
        if amount >= 0:
            return colored(str(amount), 'green')
        else:
            return colored(str(amount), 'red')

    def getAmounts(self):
        """Get income and expenses amounts."""
        self.getIncomeAmounts()
        self.getAddIncomeAmounts()
        self.getExpenseAmounts()
        self.getAddExpenseAmounts()

    def getIncomeAmounts(self):
        """Gets the amounts for all income accounts."""
        for income_account in self.income_accounts:
            income_account_name = self.getCorrectAccountName(income_account)
            self.income_amounts[income_account_name] = (
                self.getAmountForAccount(income_account)
            )

    def getAddIncomeAmounts(self):
        """Gets the amounts of the additional income accounts."""
        for add_income_account in self.add_income_accounts:
            self.income_amounts[add_income_account] = (
                self.prepareAddAmount(self.add_income_accounts[add_income_account])
            )

    def getExpenseAmounts(self):
        """Gets the amounts for all expense accounts."""
        for expense_account in self.expense_accounts:
            expense_account_name = self.getCorrectAccountName(expense_account)
            self.expense_amounts[expense_account_name] = (
                self.getAmountForAccount(expense_account)
            )

    def getAddExpenseAmounts(self):
        """Gets the amounts of the additional expense accounts."""
        for add_expense_account in self.add_expense_accounts:
            self.expense_amounts[add_expense_account] = (
                self.prepareAddAmount(self.add_expense_accounts[add_expense_account])
            )

    def getCorrectAccountName(self, account):
        """
        Gets the correct account name depengin on the accounts_name dict.
        If it's set to 'self' the account caption name will be the account itself.
        """
        try:
            if account in self.income_accounts_name:
                name = self.income_accounts_name[account]
            elif account in self.expense_accounts_name:
                name = self.expense_accounts_name[account]
            else:
                name = account
            if name.lower() == 'self':
                name = account
            return name
        except Exception as e:
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
        date_to_str = date_to.strftime('%Y-%m')

        date_from = date_to - relativedelta(months=self.months)
        date_from_str = date_from.strftime('%Y-%m')

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

    def prepareAddAmount(self, amount):
        """Convert given parameter add_account amount to Decimal, if possible."""
        try:
            return Decimal(amount)
        except Exception as e:
            return Decimal(0)
