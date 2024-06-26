"""The class holding all the settings."""

import argparse
import json


class Settings(object):
    """Settings class."""

    def __init__(
        self
    ):
        """Initialize the class and hard code defaults, if no file is given."""
        self.initArguments()
        self.variable = None

    def initArguments(self):
        self.args = argparse.ArgumentParser(
            description=(
                'A programm.'
            )
        )

        self.args.add_argument(
            'file',
            nargs='?',
            help=(
                'a ledger journal file'
            )
        )

        self.args.add_argument(
            '-e',
            '--expense',
            default=[],
            nargs='+',
            action='append',
            help=(
                'append ledger account and its name to the expense accounts array, '
                'while one account with a space should be with a single quote!'
            )
        )

        self.args.add_argument(
            '-i',
            '--income',
            default=[],
            nargs='+',
            action='append',
            help=(
                'append ledger account and its name to the income accounts array, '
                'while one account with a space should be with a single quote!'
            )
        )

        self.args.add_argument(
            '-m',
            '--months',
            default=12,
            type=int,
            help='how much months should be used for average calculation?'
        )

        self.args.add_argument(
            '-y',
            '--yearly',
            action='store_true',
            help='calculate yearly instead of monthly expenses / income'
        )

        self.args.add_argument(
            '-ai',
            '--add-income',
            default=[],
            nargs=2,
            action='append',
            help=(
                'append additional account with name and amount as '
                'an additional income account'
            )
        )

        self.args.add_argument(
            '-ae',
            '--add-expense',
            default=[],
            nargs=2,
            action='append',
            help=(
                'append additional account with name and amount as '
                'an additional expense account'
            )
        )

        self.args.add_argument(
            '-pf',
            '--period-from',
            default=False,
            help='replaces the automatic date caluclation with a "from YEAR-MONTH"'
        )

        self.args.add_argument(
            '-pt',
            '--period-to',
            default=False,
            help='replaces the automatic date caluclation with a "to YEAR-MONTH"'
        )

        self.args.add_argument(
            '-t',
            '--time',
            action='store_true',
            help='if enabled, the amount will be interpreted as a time value'
        )

        self.args.add_argument(
            '-nc',
            '--no-color',
            action='store_true',
            help='if enabled, the output will have no color'
        )

        self.args.add_argument(
            '-nt',
            '--no-total',
            action='store_true',
            help='if enabled, the output will have no total calculation'
        )

        self.args = self.args.parse_args()

    def toJson(self, indent=2, ensure_ascii=False):
        """Convert settings data to json format."""
        out = {}

        # fetch all setting variables
        out['variable'] = self.variable

        # return the json
        return json.dumps(
            out,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True
        )

    def fromJson(self, js=None):
        """Feed settings variables from json string."""
        if js is None:
            return

        # get js as dict
        try:
            js = json.loads(js)
        except Exception:
            # do not load it
            return

        # feed settings variables
        if 'variable' in js.keys():
            self.variable = js['variable']
