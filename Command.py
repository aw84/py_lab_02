import datetime

import Entry
import Repository
import settings


class Command(object):
    """
    cmd:
        list (all)
        list since <start> until <end>
        list types -- list available types of transactions
        list match <criteria>
            <criteria>:
                title <string>
                type <string>
                amount [lt,gt,eq] [value]
    """

    def run(self):
        pass

    @staticmethod
    def _parse(cmd):
        s = cmd.split()
        if s[0] == 'list':
            if len(s) == 1 or s[1] == 'all':
                end = datetime.date.today()
                start = end - datetime.timedelta(days=30)
                return ListCommand(since=start, until=end)
            elif s[1] == 'types':
                return ListEntryTypesCommand()
            elif s[1] == 'match':
                print("list match")
            elif s[1] == 'since' and s[3] == 'until':
                return ListCommand(since=settings.create_date(s[2]), until=settings.create_date(s[4]))

    @staticmethod
    def create(cmd):
        return Command._parse(cmd)


class ListEntryTypesCommand(Command):
    def __init__(self):
        super().__init__()

    def run(self):
        return [k for k in Entry.OperationMap.keys()]


class ListCommand(Command):
    def __init__(self, **kwargs):
        super().__init__()
        self.since = None
        self.until = None
        if kwargs is not None:
            for k, v in kwargs.items():
                if k == 'since':
                    self.since = v
                elif k == 'until':
                    self.until = v
        self.repository = Repository.Repository()

    def run(self):
        return self.repository.find(self.since, self.until)