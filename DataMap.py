import decimal

import settings
from domainobject.DomainObject import AccountNumber, Transaction


class DataMap(object):
    PRIMARY_KEY_FIELD = 'id'

    def __init__(self, table_name, fields):
        self.table_name = table_name
        self.fields = fields

    def get_table_name(self):
        return self.table_name

    def primary_key(self):
        return self.fields[DataMap.PRIMARY_KEY_FIELD]

    def field(self, name):
        return self.fields[name]

    def get_fields(self):
        return ','.join(self.fields.values())

    def create_from_db(self, row):
        pass

    @staticmethod
    def get_mapper(domain_object):
        if isinstance(domain_object, AccountNumber):
            return DataMapAccountNumber()
        elif isinstance(domain_object, Transaction):
            return TransactionDataMap()


class DataMapAccountNumber(DataMap):
    def __init__(self):
        super().__init__('account_numbers', {
            DataMap.PRIMARY_KEY_FIELD: 'OID',
            'number': 'NUMBER'
        })

    def create_from_db(self, row):
        o = AccountNumber()
        o.object_id = row.get_string()
        o.number = row.get_string()
        return o


class TransactionDataMap(DataMap):
    def __init__(self):
        super().__init__('transactions', {
            DataMap.PRIMARY_KEY_FIELD: 'oid',
            'tr_date': 'tr_date',
            'amount': 'amount',
            'saldo_after_tr': 'saldo_after_tr'
        })

    def create_from_db(self, row):
        o = Transaction()
        o.object_id = row.get_string()
        o.transaction_date = settings.create_date(row.get_string())
        o.amount = decimal.Decimal(row.get_string())
        o.saldo_after = decimal.Decimal(row.get_string())
        return o
