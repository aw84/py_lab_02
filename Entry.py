import Repository


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
        self.amount_ = float(row[2])
        self.saldo_after_transaction_ = float(row[3])
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


def create(row):
    if row[2] == 'PRZELEW ZEWNĘTRZNY WYCHODZĄCY' or row[2] == 'PRZELEW MTRANSFER WYCHODZACY' or row[2] == 'PRZELEW WEWNĘTRZNY WYCHODZĄCY':
        return TransferOut()
    if row[2] == 'ZAKUP PRZY UŻYCIU KARTY':
        return CartTransaction()
    if row[2] == 'PRZELEW ZEWNĘTRZNY PRZYCHODZĄCY':
        return TransferIn()
    if row[2] == '#Opis operacji':
        return MetaDescription()
    if row[2] == 'WYPŁATA W BANKOMACIE':
        return AtmTransaction()
    if row[2] == 'BLIK ZAKUP E-COMMERCE':
        return BlikTransaction()
    if row[2] == 'MOKAZJE UZNANIE':
        return MokazjeTransaction()
    other = ['OPŁATA ZA KARTĘ', 'MOKAZJE KOREKTA', 'POS ZWROT TOWARU', 'POS ZWROT TOWARU', 'OPŁATA-PRZELEW WEWN. DOWOLNY', 'RĘCZNE UZNANIE']
    if row[2] in other:
        return OtherTransaction()
    raise Exception('`'+row[2]+'\'')
