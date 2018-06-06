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
            default=None,
            help=(
                'a file'
            )
        )

        self.args.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='verbose enabled'
        )

        self.args.add_argument(
            '-d',
            '--default',
            default=None,
            help='default parameter'
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
