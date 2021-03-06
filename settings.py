from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


def create_date(string_date):
    return datetime.strptime(string_date, DATE_FORMAT).date()


def f2s(float_value):
    return '%10.2f' % float_value
