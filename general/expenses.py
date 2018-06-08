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
        add_expense_accounts=[],
        period_from=False,
        period_to=False,
        time=False
    ):
        self.ledger_file = ledger_file
        self.months = months
        self.period, self.months = self.interpretePeriods(months, period_from, period_to)
        self.yearly = yearly
        self.time = time

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
            if self.time:
                what = colored('Average yearly worktime (hours) based on', color)
            else:
                what = colored('Average yearly income / expenses based on', color)
        else:
            if self.time:
                what = colored('Average monthly worktime (hours) based on', color)
            else:
                what = colored('Average monthly income / expenses based on', color)
        months = '{} {}'.format(
            colored(self.months, color, attrs=['bold']),
            colored('months', color)
        )
        print()
        print(colored('{} {}'.format(what, months), color))
        if len(self.income_accounts) > 0:
            print()
            self.printAmounts('Income accounts', self.income_amounts, 'blue', color)
        if len(self.expense_accounts) > 0:
            print()
            self.printAmounts('Expense accounts', self.expense_amounts, 'yellow', color)
        if not self.time:
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
        if self.time:
            return self.prepareTableTime(amounts_dict, color)
        else:
            return self.prepareTableMoney(amounts_dict, color)

    def prepareTableMoney(self, amounts_dict, color):
        """Prepare the table for the money amounts."""
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

    def prepareTableTime(self, amounts_dict, color):
        """Prepare the table for the time amounts."""
        output = []
        for account in sorted(amounts_dict):
            acc_str = colored(account, color)
            amount = self.colorAmount(self.toTime(amounts_dict[account]))
            output += [[acc_str, amount]]
        output += [[
            colored('--- Total', color),
            self.colorAmount(self.toTime(sum(amounts_dict.values())))
        ]]
        return output

    def colorAmount(self, amount):
        """Depending on negative or positive, color the amount."""
        if self.time:
            return colored(str(amount), 'green')
        else:
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
        if self.time:
            return self.getAmountForAccountTime(account)
        else:
            return self.getAmountForAccountMoney(account)

    def getAmountForAccountMoney(self, account):
        """Gets the MONEY amount of the given account."""
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

    def getAmountForAccountTime(self, account):
        """Gets the TIME amount of the given account."""
        ledger_file = self.prepareLedgerFile()
        ledger_date = self.prepareLedgerDate()
        ledger_command = 'ledger {}{} --collapse b {} --format "%(total)\n"'.format(
            ledger_file, ledger_date, account
        )
        result = self.prepareTimeAmount(os.popen(ledger_command).readline().strip())
        if self.yearly:
            result = round((result / self.months) * 12, 2) * -1
        else:
            result = round(result / self.months, 2) * -1
        return result

    def toTime(self, amount):
        """Convert to readable time format 'HH:MM h'."""
        return round(amount / 3600, 2)

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
        if self.period is False:
            date_to = datetime.datetime.now()
            date_to_str = date_to.strftime('%Y-%m')

            date_from = date_to - relativedelta(months=self.months)
            date_from_str = date_from.strftime('%Y-%m')

            return '-p "from {} to {}"'.format(date_from_str, date_to_str)

        else:
            return self.period

    def prepareAmount(self, amount_str):
        """Convert the given ledger output amount string to a decimal."""
        try:
            amount_str = amount_str[2:]
            amount_str = amount_str[:amount_str.find(' ')]
            amount_str = amount_str.replace('.', '').replace(',', '.')
            return Decimal(amount_str)
        except Exception:
            return Decimal(0)

    def prepareTimeAmount(self, amount_str):
        """Convert the given ledger output amount string to a decimal."""
        try:
            amount_str = amount_str[:amount_str.find('s')]
            return Decimal(amount_str)
        except Exception:
            return Decimal(0)

    def prepareAddAmount(self, amount):
        """Convert given parameter add_account amount to Decimal, if possible."""
        try:
            return Decimal(amount)
        except Exception as e:
            return Decimal(0)

    def interpretePeriods(self, months, period_from, period_to):
        """
        Calculate months from given parameter and handle period ledger string.
        Returns a tuple with (bool|ledger-period-string, months).
        """
        if period_from is False and period_to is False:
            return (False, months)

        period_from = self.interpreteDate(period_from)
        period_to = self.interpreteDate(period_to)

        period_from, period_to = self.normalizePeriods(period_from, period_to)
        period_string = self.generatePeriodString(period_from, period_to)
        months = self.calculateMonths(period_from, period_to)

        return (period_string, months)

    def calculateMonths(self, period_from, period_to):
        """Calculate the months from two given dates.."""
        if period_from is False or period_to is False:
            return 12

        delta = relativedelta(period_to, period_from)
        return abs((delta.years * 12) + delta.months)

    def normalizePeriods(self, period_from, period_to):
        """
        Normlize the periods so that teh programm can work with them.
        Basically it tries to generate the other period with self.months months
        in difference, if only one period date is given.
        """
        if period_from is False and period_to is False:
            return (False, False)

        elif period_from is False and period_to is not False:
            period_from = period_to - relativedelta(months=self.months)

        elif period_from is not False and period_to is False:
            period_to = period_from + relativedelta(months=self.months)

        return (period_from, period_to)

    def generatePeriodString(self, period_from, period_to):
        """Generate the ledger period string from two given dates."""
        if period_from is False and period_to is False:
            return False

        str_from = period_from.strftime('%Y-%m')
        str_to = period_to.strftime('%Y-%m')

        return '-p "from {} to {}"'.format(str_from, str_to)

    def interpreteDate(self, date):
        """Interprete given date and return datetime or bool."""
        if date is False:
            return False

        try:
            return datetime.datetime.strptime(date, '%Y-%m')
        except Exception as e:
            return False
