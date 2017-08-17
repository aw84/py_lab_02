import unittest

import Entry


class ReadEntryFromCsvTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.line = ['2017-08-08', '2017-08-01', 'PRZELEW ZEWNĘTRZNY WYCHODZĄCY',
                'title', 'YYY', '11100011100011100011100011', '-100,89', '20,21']
        cls.e = Entry.Entry().from_csv(cls.line)
    def test_read_transaction_date(self):
        self.assertEqual(self.e.date(), self.line[0])
    def test_read_transaction_type(self):
        self.assertEqual(self.e.type(), self.line[2])
    def test_read_transaction_title(self):
        self.assertEqual(self.e.title(), self.line[3])
    def test_read_account_number(self):
        self.assertEqual(self.e.acc_number(), self.line[5])
    def test_read_transaction_value(self):
        self.assertEqual(self.e.amount(), -100.89)
    def test_read_saldo_after_transaction(self):
        self.assertEqual(self.e.saldo_after_transaction(), 20.21)
