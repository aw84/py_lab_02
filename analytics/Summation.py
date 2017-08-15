import Repository

class TransactionService(object):
    def find(self, begin, end):
        return Repository.Repository().find(begin, end)


class Summation(object):
    """description of class"""
    def sum(self, begin, end):
        entries = TransactionService().find(begin, end)
        s = 0.0
        for e in entries:
            s = s + e.amount()
        return s