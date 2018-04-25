from datetime import date

import Entry
import Repository


class TransactionService(object):
    def __init__(self, **kwargs):
        self.repository = Repository.Repository()
        return super().__init__(**kwargs)
    def find(self, begin, end):
        return self.repository.find(begin, end)
    def find_transfer(self, begin, end, account_number):
        return self.repository.find_transfer(begin, end, account_number)
    def find_by_criteria(self, a_criteria):
        return self.repository.find_by_criteria(a_criteria)

class Summation(object):
    """description of class"""
    def __init__(self, **kwargs):
        self.account_period_start = 25
        return super().__init__(**kwargs)
    def _sum(self, begin, end):
        entries = TransactionService().find(begin, end)
        s = 0.0
        for e in entries:
            s = s + e.amount()
        return s
    def sum_year(self, year):
        return self._sum(date(year, 1, self.account_period_start),
                         date(year + 1, 1, self.account_period_start))
    def sum_month(self, year, month):
        if month == 12:
            return self._sum(date(year, month, self.account_period_start),
                             date(year + 1, 1, self.account_period_start))
        else:
            return self._sum(date(year, month, self.account_period_start),
                             date(year, month + 1, self.account_period_start))
    def sum_year_transfer_amount(self, year, account_number):
        entries = TransactionService().find_transfer(date(year, 1, self.account_period_start),
                                                     date(year + 1, 1, self.account_period_start),
                                                     account_number)
        s = 0.0
        for e in entries:
            if (Entry.OperationMap[e.type()] == Entry.OperationType.TRANSFER_OUT
                or Entry.OperationMap[e.type()] == Entry.OperationType.TRANSFER_IN) and e.acc_number() == account_number:
                s += e.amount()
        return s
