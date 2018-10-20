from decimal import Decimal
from termcolor import colored


def colorAmount(time, amount, no_color):
    """Depending on negative or positive, color the amount."""
    if no_color:
        return str(amount)
    if time:
        return colored(str(amount), 'green')
    else:
        if amount >= 0:
            return colored(str(amount), 'green')
        else:
            return colored(str(amount), 'red')


def getCorrectAccountName(accounts_name_dict, account):
    """
    Gets the correct account name depending on the accounts_name dict.
    If it's set to 'self' the account caption name will be the account itself.
    """
    try:
        if account in accounts_name_dict:
            name = accounts_name_dict[account]
        else:
            name = account
        if name.lower() == 'self':
            name = account
        return name
    except Exception as e:
        return account


def prepareMoneyAmount(amount_str):
    """Convert the given ledger output amount string to a decimal."""
    try:
        amount_str = amount_str[2:]
        amount_str = amount_str[:amount_str.find(' ')]
        amount_str = amount_str.replace('.', '').replace(',', '.')
        return Decimal(amount_str)
    except Exception:
        return Decimal(0)


def prepareTimeAmount(amount_str):
    """Convert the given ledger output amount string to a decimal."""
    try:
        amount_str = amount_str[:amount_str.find('s')]
        return Decimal(amount_str)
    except Exception:
        return Decimal(0)


def prepareAddAmount(amount):
    """Convert given parameter add_account amount to Decimal, if possible."""
    try:
        return Decimal(amount)
    except Exception as e:
        return Decimal(0)


def toTime(amount):
    """Convert from seconds to 'HH:MM h' format."""
    decimal_time = round(amount / 3600, 2)
    hours, minutes = divmod(decimal_time, 1)
    minutes = int(minutes * 60)
    return '{}:{:02} h'.format(hours, minutes)
