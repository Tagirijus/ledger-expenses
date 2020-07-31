import datetime
from dateutil.relativedelta import relativedelta


def generatePeriodString(period_from, period_to):
    """Generate the ledger period string from two given dates."""
    if period_from is False and period_to is False:
        return False

    str_from = period_from.strftime('%Y-%m')
    str_to = period_to.strftime('%Y-%m')

    return '-p "from {} to {}"'.format(str_from, str_to)


def prepareLedgerDate(period, months):
    """
    Prepare the ledger date according to the months and output
    the ledger parameter.
    """
    if period is False:
        date_to = datetime.datetime.now()
        date_to_str = date_to.strftime('%Y-%m')

        date_from = date_to - relativedelta(months=months)
        date_from_str = date_from.strftime('%Y-%m')

        return '-p "from {} to {}"'.format(date_from_str, date_to_str)

    else:
        return period


def prepareLedgerFile(ledger_file):
    """Outputs the ledger file, if given."""
    if ledger_file is not None:
        return '-f {} '.format(ledger_file)
    else:
        return ''
