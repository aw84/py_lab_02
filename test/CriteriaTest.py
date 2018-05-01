import decimal
import unittest

import Repository
import settings
from Criteria import Criteria, BetweenCriteria
from DataMap import DataMap
from Repository import Repository2
from domainobject.DomainObject import AccountNumber, Transaction

"""
CREATE TABLE transactions(oid text, tr_date date, amount real, saldo_after_tr real);
CREATE TABLE transaction_details(tr_oid text, type text, title text, tr_date date);

CREATE TABLE account_numbers(oid text, number text);
CREATE TABLE transfer_log(tr_oid text, acc_oid text);

CREATE TABLE categories(oid text, cname text);
CREATE TABLE transaction_category(tr_oid, cat_oid);
"""


class AccountNumberTest(unittest.TestCase):
    def test_set_object_id(self):
        a = AccountNumber()
        a.object_id = 'abc'
        self.assertEqual('abc', a.object_id)

    def test_set_account_number(self):
        a = AccountNumber()
        a.number = 'xyz'
        self.assertEqual('xyz', a.number)


class TransactionTests(unittest.TestCase):
    def test_set_transaction_date(self):
        t = Transaction()
        test_date = '2018-04-27'
        t.transaction_date = settings.create_date(test_date)
        self.assertEqual(settings.create_date(test_date), t.transaction_date)

    def test_set_amount(self):
        t = Transaction()
        test_amount = 10.23
        t.amount = decimal.Decimal(test_amount)
        self.assertEqual(decimal.Decimal(test_amount), t.amount)

    def test_set_saldo(self):
        t = Transaction()
        test_saldo = 22.3
        t.saldo_after = decimal.Decimal(test_saldo)
        self.assertEqual(decimal.Decimal(test_saldo), t.saldo_after)


class DataMapTest(unittest.TestCase):
    def test_creation(self):
        o = AccountNumber()
        data_map = DataMap.get_mapper(o)
        self.assertEqual('account_numbers', data_map.get_table_name())

    def test_fields_generation(self):
        data_map = DataMap.get_mapper(AccountNumber())
        self.assertEqual('OID,NUMBER', data_map.get_fields())


class TestableDataMap(DataMap):
    def __init__(self):
        super().__init__('test_table_name', {
            'id': 'DB_NAME1',
            'field1': 'DB_NAME2'
        })


class CriteriaTest(unittest.TestCase):
    def test_equal(self):
        criteria = Criteria.equal(number='dddddd')
        repository = Repository.Repository()
        repository.find_by_criteria(criteria)
        self.assertTrue(True)

    def test_between(self):
        criteria = BetweenCriteria()
        criteria.add_condition('id', '<', 'value_1')
        criteria.add_condition('field1', '>', 'value_2')
        criteria.set_join_function('AND')
        self.assertEqual('(DB_NAME1<? AND DB_NAME2>?)', criteria.str(TestableDataMap()))
        self.assertEqual(('value_1', 'value_2'), criteria.values())


class RepositoryTests(unittest.TestCase):
    def test_query_preparation_with_criteria(self):
        data_map = TestableDataMap()
        repo = Repository2(data_map)
        ret = repo.query_preparation(Criteria.equal(id='xxx'))
        self.assertEqual('select DB_NAME1,DB_NAME2 from test_table_name where DB_NAME1=xxx', ret)

    def test_query_preparation(self):
        data_map = TestableDataMap()
        repo = Repository2(data_map)
        ret = repo.query_preparation()
        self.assertEqual('select DB_NAME1,DB_NAME2 from test_table_name', ret)
