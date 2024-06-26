import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from general import date_helper
from general import ledger_helper
from general import helper
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
        time=False,
        no_color=False,
        no_total=False
    ):
        self.ledger_file = ledger_file
        self.months = months
        self.period, self.months = self.interpretePeriods(months, period_from, period_to)
        self.yearly = yearly
        self.time = time
        self.no_color = no_color
        self.no_total = no_total

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

    def interpretePeriods(self, months, period_from, period_to):
        """
        Calculate months from given parameter and handle period ledger string.
        Returns a tuple with (bool|ledger-period-string, months).
        """
        if period_from is False and period_to is False:
            return (False, months)

        period_from = date_helper.interpreteDate(period_from)
        period_to = date_helper.interpreteDate(period_to)

        period_from, period_to = date_helper.normalizePeriods(
            self.months, period_from, period_to
        )
        period_string = ledger_helper.generatePeriodString(period_from, period_to)
        months = date_helper.calculateMonths(period_from, period_to)

        return (period_string, months)

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
            if len(account) < 2:
                name[account[0]] = account[0]
            else:
                name[account[0]] = account[1]
        return (acc, name)

    def getAmounts(self):
        """Get income and expenses amounts."""
        self.getIncomeAmounts()
        self.getAddIncomeAmounts()
        self.getExpenseAmounts()
        self.getAddExpenseAmounts()

    def getIncomeAmounts(self):
        """Gets the amounts for all income accounts."""
        for income_account in self.income_accounts:
            income_account_name = helper.getCorrectAccountName(
                self.income_accounts_name, income_account
            )
            self.income_amounts[income_account_name] = (
                self.getAmountForAccount(income_account)
            )

    def getAddIncomeAmounts(self):
        """Gets the amounts of the additional income accounts."""
        for add_income_account in self.add_income_accounts:
            self.income_amounts[add_income_account] = (
                helper.prepareAddAmount(self.add_income_accounts[add_income_account])
            )

    def getExpenseAmounts(self):
        """Gets the amounts for all expense accounts."""
        for expense_account in self.expense_accounts:
            expense_account_name = helper.getCorrectAccountName(
                self.expense_accounts_name, expense_account
            )
            self.expense_amounts[expense_account_name] = (
                self.getAmountForAccount(expense_account)
            )

    def getAddExpenseAmounts(self):
        """Gets the amounts of the additional expense accounts."""
        for add_expense_account in self.add_expense_accounts:
            self.expense_amounts[add_expense_account] = (
                helper.prepareAddAmount(self.add_expense_accounts[add_expense_account])
            )

    def getAmountForAccount(self, account):
        """Gets the amount of the given account."""
        if self.time:
            return self.getAmountForTimeAccount(account)
        else:
            return self.getAmountForMoneyAccount(account)

    def getAmountForMoneyAccount(self, account):
        """Gets the MONEY amount of the given account."""
        ledger_file = ledger_helper.prepareLedgerFile(self.ledger_file)
        ledger_date = ledger_helper.prepareLedgerDate(self.period, self.months)
        ledger_command = 'ledger {}{} --collapse b {}'.format(
            ledger_file, ledger_date, account
        )
        result = helper.prepareMoneyAmount(os.popen(ledger_command).readlines())
        if self.yearly:
            result = round((result / self.months) * 12, 2) * -1
        else:
            result = round(result / self.months, 2) * -1
        return result

    def getAmountForTimeAccount(self, account):
        """Gets the TIME amount of the given account."""
        ledger_file = ledger_helper.prepareLedgerFile(self.ledger_file)
        ledger_date = ledger_helper.prepareLedgerDate(self.period, self.months)
        ledger_command = 'ledger {}{} --collapse b {} --format "%(total)\n"'.format(
            ledger_file, ledger_date, account
        )
        result = helper.prepareTimeAmount(os.popen(ledger_command).readline().strip())
        if self.yearly:
            result = round((result / self.months) * 12, 2)
        else:
            result = round(result / self.months, 2)
        return result

    def show(self, color='white'):
        """Output the main results."""
        if self.yearly:
            if self.time:
                what = (
                    'Average yearly worktime (hours) based on'
                    if self.no_color else
                    colored('Average yearly worktime (hours) based on', color)
                )
            else:
                what = (
                    'Average yearly income / expenses based on'
                    if self.no_color else
                    colored('Average yearly income / expenses based on', color)
                )
        else:
            if self.time:
                what = (
                    'Average monthly worktime (hours) based on'
                    if self.no_color else
                    colored('Average monthly worktime (hours) based on', color)
                )
            else:
                what = (
                    'Average monthly income / expenses based on'
                    if self.no_color else
                    colored('Average monthly income / expenses based on', color)
                )
        months = (
            '{} months'.format(self.months)
            if self.no_color else
            '{} {}'.format(
                colored(self.months, color, attrs=['bold']),
                colored('months', color)
            )
        )
        print()
        if self.no_color:
            print('{} {}'.format(what, months))
        else:
            print(colored('{} {}'.format(what, months), color))
        if len(self.income_accounts) > 0:
            print()
            self.printAmounts('Income accounts', self.income_amounts, 'blue', color)
        if len(self.expense_accounts) > 0:
            print()
            self.printAmounts('Expense accounts', self.expense_amounts, 'yellow', color)
        if not self.time and not self.no_total:
            print()
            print()
            self.printBoth(color)
        print()

    def printBoth(self, gui_color='white'):
        """Print the income versus the expenses."""
        income_total = sum(self.income_amounts.values())
        expense_total = sum(self.expense_amounts.values())
        total = income_total + expense_total
        if self.no_color:
            print('{} {}'.format(
                'Total money flow:',
                helper.colorAmount(self.time, total, self.no_color)
            ))
        else:
            print('{} {}'.format(
                colored('Total money flow:', gui_color),
                helper.colorAmount(self.time, total, self.no_color)
            ))

    def printAmounts(self, title, amounts_dict, color, gui_color='white'):
        """Print an amounts dict as a table."""
        if self.no_color:
            print(
                tabulate(
                    self.prepareTable(amounts_dict, color),
                    headers=[title, '€'],
                    tablefmt='plain'
                )
            )
        else:
            print(
                tabulate(
                    self.prepareTable(amounts_dict, color),
                    headers=[colored(title, gui_color), colored('€', gui_color)],
                    tablefmt='plain'
                )
            )

    def prepareTable(self, amounts_dict, color):
        """Prepare the table for the money amounts."""
        output = []
        for account in sorted(amounts_dict):
            if account == 'Total':
                continue
            acc_str = (
                account
                if self.no_color else
                colored(account, color)
            )
            if self.time:
                amount = helper.colorAmount(
                    self.time, helper.toTime(amounts_dict[account]),
                    self.no_color
                )
            else:
                amount = helper.colorAmount(
                    self.time, amounts_dict[account], self.no_color
                )
            output += [[acc_str, amount]]
        if not self.no_total:
            output = self.prepareTotal(amounts_dict, output, color)
        return output

    def prepareTableTotal(self, amounts_dict):
        """Check if 'Total' exists in the dict, otherwise sum the values."""
        if 'Total' in amounts_dict:
            total = amounts_dict['Total']
        else:
            total = sum(amounts_dict.values())

        if self.time:
            total = helper.toTime(total)

        return total

    def prepareTotal(self, amounts_dict, output, color):
        total = self.prepareTableTotal(amounts_dict)
        if self.no_color:
            output += [[
                '--- Total',
                helper.colorAmount(self.time, total, self.no_color)
            ]]
        else:
            output += [[
                colored('--- Total', color),
                helper.colorAmount(self.time, total, self.no_color)
            ]]
        return output
