import Repository


class Entry:
    def __init__(self, row):
        self.transaction_date = row[0]
        self.account_date = row[1]
        self.entry_type = row[2]
        self.title_ = row[3]
        self.account_number = row[5].strip('\'')
        self.amount_ = row[6]
        self.saldo_after_transaction_ = row[7]
        self.str = ''
    def print(self):
        print(self.str, flush=True)
    def acc_number(self):
        return self.account_number
    def repository(self):
        return None
    def date(self):
        return self.transaction_date
    def amount(self):
        a = self.amount_.replace(',','.').replace(' ','')
        return float(a)
    def type(self):
        return self.entry_type
    def title(self):
        return self.title_
    def saldo_after_transaction(self):
        s = self.saldo_after_transaction_.replace(',','.').replace(' ','')
        return float(s)


class TransferOut(Entry):
    def __init__(self, row):
        super().__init__(row)
        self.str = "{acc_number} {amount}".format(acc_number=self.account_number, amount=self.amount())
    def repository(self):
        return Repository.TransferRepository()


class TransferIn(Entry):
    def __init__(self, row):
        super().__init__(row)
        self.str = "{acc_number} {amount}".format(acc_number=self.account_number, amount=self.amount())
    def repository(self):
        return Repository.TransferRepository()


class CartTransaction(Entry):
    def __init__(self, row):
        super().__init__(row)
    def repository(self):
        return Repository.CartTransactionRepository()


class MetaDescription(Entry):
    def __init__(self, row):
        super().__init__(row)
        self.str = ' '.join(row)
    def acc_number(self):
        return ''
    def repository(self):
        raise Exception("MetaRepository not implemented")


class AtmTransaction(Entry):
    def __init__(self, row):
        super().__init__(row)
    def repository(self):
        return Repository.AtmRepository()


class BlikTransaction(Entry):
    def __init__(self, row):
        super().__init__(row)
    def repository(self):
        raise Exception("BlikRepository not implemented")


class OtherTransaction(Entry):
    def __init__(self, row):
        super().__init__(row)
    def repository(self):
        raise Exception("OtherRepository not implemented")


class MokazjeTransaction(Entry):
    def __init__(self, row):
        super().__init__(row)
    def repository(self):
        raise Exception("MokazjeRepository not implemented")


def create(row):
    if row[2] == 'PRZELEW ZEWNĘTRZNY WYCHODZĄCY' or row[2] == 'PRZELEW MTRANSFER WYCHODZACY' or row[2] == 'PRZELEW WEWNĘTRZNY WYCHODZĄCY':
        return TransferOut(row)
    if row[2] == 'ZAKUP PRZY UŻYCIU KARTY':
        return CartTransaction(row)
    if row[2] == 'PRZELEW ZEWNĘTRZNY PRZYCHODZĄCY':
        return TransferIn(row)
    if row[2] == '#Opis operacji':
        return MetaDescription(row)
    if row[2] == 'WYPŁATA W BANKOMACIE':
        return AtmTransaction(row)
    if row[2] == 'BLIK ZAKUP E-COMMERCE':
        return BlikTransaction(row)
    if row[2] == 'MOKAZJE UZNANIE':
        return MokazjeTransaction(row)
    other = ['OPŁATA ZA KARTĘ', 'MOKAZJE KOREKTA', 'POS ZWROT TOWARU', 'POS ZWROT TOWARU', 'OPŁATA-PRZELEW WEWN. DOWOLNY', 'RĘCZNE UZNANIE']
    if row[2] in other:
        return OtherTransaction(row)
    raise Exception('`'+row[2]+'\'')
