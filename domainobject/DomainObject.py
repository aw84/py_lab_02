class DomainObject(object):
    def __init__(self):
        super().__init__()
        self.__object_id = None

    @property
    def object_id(self):
        return self.__object_id

    @object_id.setter
    def object_id(self, value):
        self.__object_id = value


class AccountNumber(DomainObject):
    def __init__(self):
        super().__init__()
        self.__number = None

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        self.__number = value


class Transaction(DomainObject):
    def __init__(self):
        super().__init__()
        self.__transaction_date = None
        self.__amount = None
        self.__saldo_after = None

    @property
    def transaction_date(self):
        return self.__transaction_date

    @transaction_date.setter
    def transaction_date(self, value):
        self.__transaction_date = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        self.__amount = value

    @property
    def saldo_after(self):
        return self.__saldo_after

    @saldo_after.setter
    def saldo_after(self, value):
        self.__saldo_after = value
