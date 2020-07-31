import datetime
from dateutil.relativedelta import relativedelta


def calculateMonths(period_from, period_to):
    """Calculate the months from two given dates.."""
    if period_from is False or period_to is False:
        return 12

    delta = relativedelta(period_to, period_from)
    return abs((delta.years * 12) + delta.months)


def interpreteDate(date):
    """Interprete given date and return datetime or bool."""
    if date is False:
        return False

    try:
        return datetime.datetime.strptime(date, '%Y-%m')
    except Exception as e:
        return False


def normalizePeriods(months, period_from, period_to):
    """
    Normlize the periods so that teh programm can work with them.
    Basically it tries to generate the other period with self.months months
    in difference, if only one period date is given.
    """
    if period_from is False and period_to is False:
        return (False, False)

    elif period_from is False and period_to is not False:
        period_from = period_to - relativedelta(months=months)

    elif period_from is not False and period_to is False:
        period_to = period_from + relativedelta(months=months)

    return (period_from, period_to)
