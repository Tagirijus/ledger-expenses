class Expenses(object):

    def __init__(self, settings):
        self.settings = settings

    def showFile(self):
        print(self.settings.args.file)
