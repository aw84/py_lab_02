import datetime
import unittest

from Command import Command, ListCommand


class CommandParserTest(unittest.TestCase):
    def _list_all_assertions(self, cmd):
        self.assertTrue(isinstance(cmd, ListCommand))
        self.assertTrue(isinstance(cmd.since, datetime.date))
        self.assertTrue(isinstance(cmd.until, datetime.date))

    def test_list_all_implicit(self):
        cmd = Command.create('list')
        self._list_all_assertions(cmd)

    def test_list_all_explicit(self):
        cmd = Command.create('list all')
        self._list_all_assertions(cmd)

    def test_list_period_of_time(self):
        since_date = '2017-01-01'
        until_date = '2017-03-31'
        cmd = Command.create('list since {since} until {until}'.format(since=since_date, until=until_date))
        self.assertTrue(isinstance(cmd, ListCommand))
        self.assertEqual(cmd.since, datetime.date(2017, 1, 1))
        self.assertEqual(cmd.until, datetime.date(2017, 3, 31))

    def test_list_entry_types(self):
        lst = Command.create('list types').run()
        self.assertTrue(len(lst) > 0)
