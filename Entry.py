import Repository
from enum import Enum


class Entry:
    def __init__(self):
        self.transaction_date = None
        self.account_date = None
        self.entry_type = None
        self.title_ = None
        self.account_number = None
        self.amount_ = None
        self.saldo_after_transaction_ = None
        self.str = None
        self.oid_ = None
    def from_csv(self, line):
        self.transaction_date = line[0]
        self.account_date = line[1]
        self.entry_type = line[2]
        self.title_ = line[3]
        self.account_number = line[5].strip('\'')
        self.amount_ = float(line[6].replace(',','.').replace(' ',''))
        self.saldo_after_transaction_ = float(line[7].replace(',','.').replace(' ',''))
        self.str = ''
        self.oid_ = None
        return self
    def from_db(self, row):
        self.oid_ = row[0]
        self.transaction_date = row[1]
        self.account_date = row[2]
        self.entry_type = row[3]
        self.title_ = row[4]
        self.account_number = row[5]
        self.amount_ = row[6]
        self.saldo_after_transaction_ = row[7]
        return self
    def oid(self, oid=None):
        if oid is None:
            return self.oid_
        self.oid_ = oid
    def print(self):
        print(self.str, flush=True)
    def acc_number(self):
        return self.account_number
    def repository(self):
        return None
    def date(self):
        return self.transaction_date
    def amount(self):
        return self.amount_
    def type(self):
        return self.entry_type
    def title(self):
        return self.title_
    def saldo_after_transaction(self):
        return self.saldo_after_transaction_


class TransferOut(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        super().from_csv(line)
        self.str = "{acc_number} {amount}".format(acc_number=self.account_number, amount=self.amount())
        return self
    def from_db(self, row):
        return super().from_db(row)
    def repository(self):
        return Repository.TransferRepository()


class TransferIn(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        super().from_csv(line)
        self.str = "{acc_number} {amount}".format(acc_number=self.account_number, amount=self.amount())
        return self
    def from_db(self, row):
        return super().from_db(row)
    def repository(self):
        return Repository.TransferRepository()


class CartTransaction(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        return super().from_csv(line)
    def from_db(self, row):
        return super().from_db(row)
    def repository(self):
        return Repository.CartTransactionRepository()


class MetaDescription(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        self.transaction_date = line[0]
        self.account_date = line[1]
        self.entry_type = line[2]
        self.title_ = line[3]
        self.account_number = line[5]
        self.amount_ = line[6]
        self.saldo_after_transaction_ = line[7]
        self.str = ''
        self.oid_ = None
        return self
        self.str = ' '.join(row)
        return self
    def from_db(self, row):
        return super().from_db(row)
    def acc_number(self):
        return ''
    def repository(self):
        raise Exception("MetaRepository not implemented")


class AtmTransaction(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        return super().from_csv(line)
    def from_db(self, row):
        return super().from_db(row)
    def repository(self):
        return Repository.AtmRepository()


class BlikTransaction(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        return super().from_csv(line)
    def from_db(self, row):
        return super().from_db(row)
    def repository(self):
        raise Exception("BlikRepository not implemented")


class OtherTransaction(Entry):
    def __init__(self):
        super().__init__()
    def from_csv(self, line):
        return super().from_csv(line)
    def from_db(self, row):
        return super().from_db(row)
    def repository(self):
        raise Exception("OtherRepository not implemented")


class MokazjeTransaction(Entry):
    def __init__(self):
        super().__init__()
    def repository(self):
        raise Exception("MokazjeRepository not implemented")


class EntryFactory(object):
    def from_csv(self, line):
        operation_name = line[2]
        ot = OperationMap[operation_name]
        if ot == OperationType.TRANSFER_OUT:
            e = TransferOut()
        elif ot == OperationType.CART_TRANSACTION:
            e = CartTransaction()
        elif ot == OperationType.TRANSFER_IN:
            e = TransferIn()
        elif ot == OperationType.META_DESCRIPTION:
            e = MetaDescription()
        elif ot == OperationType.ATM_TRANSACTION:
            e = AtmTransaction()
        elif ot == OperationType.BLIK_TRANSACTION:
            e = BlikTransaction()
        elif ot == OperationType.MOKAZJE_TRANSACTION:
            e = MokazjeTransaction()
        elif ot == OperationType.OTHER:
            e = OtherTransaction()
        else:
            raise Exception('Unknown opration type: `' + operation_name + '\'')
        e.from_csv(line)
        return e
    def from_db(row):
        pass


class OperationType(Enum):
    TRANSFER_OUT = 1,
    CART_TRANSACTION = 2,
    TRANSFER_IN = 3,
    META_DESCRIPTION = 4,
    ATM_TRANSACTION = 5,
    BLIK_TRANSACTION = 6,
    MOKAZJE_TRANSACTION = 7,
    OTHER = 9999


OperationMap = {
    'PRZELEW ZEWNĘTRZNY WYCHODZĄCY': OperationType.TRANSFER_OUT,
    'PRZELEW MTRANSFER WYCHODZACY': OperationType.TRANSFER_OUT,
    'PRZELEW WEWNĘTRZNY WYCHODZĄCY': OperationType.TRANSFER_OUT,
    'ZAKUP PRZY UŻYCIU KARTY': OperationType.CART_TRANSACTION,
    'PRZELEW ZEWNĘTRZNY PRZYCHODZĄCY': OperationType.TRANSFER_IN,
    '#Opis operacji': OperationType.META_DESCRIPTION,
    'WYPŁATA W BANKOMACIE': OperationType.ATM_TRANSACTION,
    'BLIK ZAKUP E-COMMERCE': OperationType.BLIK_TRANSACTION,
    'MOKAZJE UZNANIE': OperationType.MOKAZJE_TRANSACTION,
    'OPŁATA ZA KARTĘ': OperationType.OTHER,
    'MOKAZJE KOREKTA': OperationType.OTHER,
    'POS ZWROT TOWARU': OperationType.OTHER,
    'POS ZWROT TOWARU': OperationType.OTHER,
    'OPŁATA-PRZELEW WEWN. DOWOLNY': OperationType.OTHER,
    'RĘCZNE UZNANIE': OperationType.OTHER,
    }


def create_from_csv(line):
    f = EntryFactory()
    return f.from_csv(line)
