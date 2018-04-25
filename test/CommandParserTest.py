import datetime
import unittest

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
                return ListCommand(count=300)
            elif s[1] == 'types':
                return ListEntryTypesCommand()
            elif s[1] == 'match':
                print("list match")
            elif s[1] == 'since' and s[3] == 'until':
                return ListCommand(since=s[2], until=s[4])

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
        self.count = 0
        self.since = None
        self.until = None
        if kwargs is not None:
            for k, v in kwargs.items():
                if k == 'count':
                    self.count = int(v)
                elif k == 'since':
                    self.since = settings.create_date(v)
                elif k == 'until':
                    self.until = settings.create_date(v)
        self.repository = Repository.Repository()

    def run(self):
        return self.repository.find(self.since, self.until)


class CommandParserTest(unittest.TestCase):
    def test_list_all_implicit(self):
        self.assertTrue(isinstance(Command.create('list'), ListCommand))

    def test_list_all_explicit(self):
        self.assertTrue(isinstance(Command.create('list all'), ListCommand))

    def test_list_period_of_time(self):
        since_date = '2017-01-01'
        until_date = '2017-03-31'
        cmd = Command.create('list since {since} until {until}'.format(since=since_date, until=until_date))
        self.assertTrue(isinstance(cmd, ListCommand))
        self.assertEqual(cmd.since, datetime.date(2017, 1, 1))
        self.assertEqual(cmd.until, datetime.date(2017, 3, 31))
        self.assertEqual(cmd.count, 0)

    def test_list_entry_types(self):
        lst = Command.create('list types').run()
        self.assertTrue(len(lst) > 0)
