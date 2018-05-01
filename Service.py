import datetime

import Criteria
import DataMap
import Repository
from domainobject import DomainObject


class AbstractService(object):
    def __init__(self, data_map):
        self.repository = Repository.Repository2(data_map)


class Transaction(AbstractService):
    """
    CREATE TABLE transactions(oid text, tr_date date, amount real, saldo_after_tr real);
    """

    def __init__(self):
        super().__init__(DataMap.DataMap.get_mapper(DomainObject.Transaction()))

    def find_by(self, criteria):
        return self.repository.find_by_criteria(criteria)

    def get_month_to_date(self, end_date):
        start_date = end_date - datetime.timedelta(days=180)
        criteria = Criteria.BetweenCriteria()
        criteria.set_join_function('and')
        criteria.add_condition('tr_date', '>=', start_date)
        criteria.add_condition('tr_date', '<=', end_date)
        return self.repository.find_by_criteria(criteria)

    def get_year_to_date(self):
        pass

    def get_month_to_month(self, month):
        pass

    def get_year_to_year(self, year):
        pass
