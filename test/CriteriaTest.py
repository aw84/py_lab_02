import unittest

import Repository

"""
CREATE TABLE account_numbers(oid text, number text);
CREATE TABLE transactions(oid text, tr_date date, amount real, saldo_after_tr real);
CREATE TABLE transaction_details(tr_oid text, type text, title text, tr_date date);
CREATE TABLE transfer_log(tr_oid text, acc_oid text);
CREATE TABLE categories(oid text, cname text);
CREATE TABLE transaction_category(tr_oid, cat_oid);
"""


class DomainObject(object):
    pass


class AccountNumber(DomainObject):
    pass


class DataMap(object):
    def __init__(self):
        self.table_name = None
        self.fields = {}

    def get_table_name(self):
        return self.table_name

    def primary_key(self):
        return self.fields['ID']

    def field(self, name):
        return self.fields[name]

    def get_fields(self):
        return ','.join(self.fields.values())

    @staticmethod
    def get(o):
        if isinstance(o, AccountNumber):
            return DataMapAccountNumber()


class DataMapAccountNumber(DataMap):
    def __init__(self):
        super().__init__()
        self.table_name = 'account_numbers'
        self.fields = {
            'ID': 'OID',
            'NUMBER': 'NUMBER'
        }


class Criteria(object):
    """
    criteria = Criteria.equal(title='some string')
    repository = Repository()
    objects_list = repository.find_by_criteria(criteria)
    """

    def __init__(self):
        self.operator = None

    def equal(self, **kwargs):
        for k, v in kwargs.items():
            return EqualCriteria('=', k, v)

    def str(self, data_map):
        pass


class EqualCriteria(Criteria):
    def __init__(self, op, field, value):
        super().__init__()
        self.operator = op
        self.field = field
        self.value = value

    def str(self, data_map):
        return '{field}{operator}{value}'.format(field=data_map.field(self.field), operator=self.operator,
                                                 value=self.value)


class Repository2(object):
    def __init__(self, data_map):
        self.data_map = data_map

    def find(self):
        query = 'select {fields} from {table}'.format(
            fields=self.data_map.get_fields(), table=self.data_map.get_table_name()
        )
        return query

    def find_by_criteria(self, criteria):
        query = 'select {fields} from {table} where {a_criteria}'.format(
            fields=self.data_map.get_fields(), table=self.data_map.get_table_name(),
            a_criteria=criteria.str(self.data_map)
        )
        return query


class DataMapTest(unittest.TestCase):
    def test_creation(self):
        o = AccountNumber()
        data_map = DataMap.get(o)
        self.assertEqual('account_numbers', data_map.get_table_name())

    def test_fields_generation(self):
        data_map = DataMap.get(AccountNumber())
        self.assertEqual('OID,NUMBER', data_map.get_fields())


class CriteriaTest(unittest.TestCase):
    def test_sample(self):
        criteria = Criteria().equal(number='dddddd')
        repository = Repository.Repository()
        repository.find_by_criteria(criteria)
        self.assertTrue(True)


class TestableDataMap(DataMap):
    def __init__(self):
        super().__init__()
        self.table_name = 'test_table_name'
        self.fields = {
            'APP_NAME1': 'DB_NAME1',
            'APP_NAME2': 'DB_NAME2'
        }


class RepositoryTests(unittest.TestCase):
    def test_sample(self):
        data_map = TestableDataMap()
        repo = Repository2(data_map)
        crit = Criteria().equal(APP_NAME1='xxx')
        crit.str(data_map)
        ret = repo.find_by_criteria(crit)
        self.assertEqual('select DB_NAME1,DB_NAME2 from test_table_name where DB_NAME1=xxx', ret)
