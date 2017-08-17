import unittest

import Entry


class ReadEntryFromDbTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = ['OID', '2017-08-08', '2017-08-01', 'PRZELEW ZEWNĘTRZNY WYCHODZĄCY',
                'title', '11100011100011100011100011', -100.89, 20.21]
        cls.e = Entry.Entry().from_db(cls.row)
    def test_read_entry_oid(self):
        self.assertEqual(self.e.oid(), 'OID')
    def test_read_transaction_date(self):
        self.assertEqual(self.e.date(), '2017-08-08')
    def test_read_transaction_type(self):
        self.assertEqual(self.e.type(), 'PRZELEW ZEWNĘTRZNY WYCHODZĄCY')
    def test_read_transaction_title(self):
        self.assertEqual(self.e.title(), 'title')
    def test_read_account_number(self):
        self.assertEqual(self.e.acc_number(), '11100011100011100011100011')
    def test_read_transaction_value(self):
        self.assertEqual(self.e.amount(), -100.89)
    def test_read_saldo_after_transaction(self):
        self.assertEqual(self.e.saldo_after_transaction(), 20.21)