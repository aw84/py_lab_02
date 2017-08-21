from datetime import date

import Entry
import Repository


class TransactionService(object):
    def __init__(self, **kwargs):
        self.repository = Repository.Repository()
        return super().__init__(**kwargs)
    def find(self, begin, end):
        return self.repository.find(begin, end)

class Summation(object):
    """description of class"""
    def _sum(self, begin, end=None):
        entries = TransactionService().find(begin, end)
        s = 0.0
        for e in entries:
            s = s + e.amount()
        return s
    def sum_year(self, year):
        return self._sum(date(year, 1, 1), date(year + 1, 1, 1))
    def sum_month(self, year, month):
        if month == 12:
            return self._sum(date(year, month, 1), date(year + 1, 1, 1))
        else:
            return self._sum(date(year, month, 1), date(year, month + 1, 1))