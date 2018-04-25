from datetime import date
import statistics

import analytics.Summation


def f2s(float_value):
    return '%10.2f' % float_value


class CalcPack(object):
    def __init__(self, data):
        self.data = data
    def __str__(self):
        s = "cnt: %5d md_gr: %s median: %s stdev: %s mean: %s sum: %s" % (
            self.count(),
            f2s(self.median_grouped()),
            f2s(self.median()),
            f2s(self.stdev()),
            f2s(self.mean()),
            f2s(self.sum())
            )
        return s
    def count(self):
        return len(self.data)
    def median_grouped(self, interval=3):
        return statistics.median_grouped(self.data, interval)
    def median(self):
        return statistics.median_low(self.data)
    def stdev(self):
        try:
            return statistics.stdev(self.data)
        except statistics.StatisticsError:
            return 0
    def mean(self):
        return statistics.mean(self.data)
    def sum(self):
        s = 0.0
        for d in self.data:
            s += d
        return s

        
def calc_period(begin, end):
    ts = analytics.Summation.TransactionService()
    entries = ts.find(begin, end)
    if len(entries) == 0:
        return None, None
    expences = []
    income = []
    for e in entries:
        if e.amount() < 0:
            expences.append(e.amount())
        else:
            income.append(e.amount())
    return CalcPack(expences), CalcPack(income)


def calculate_interval(year_begin, year_end, month_interval, period_start = 25):
    result = []
    for year in range(year_begin, year_end):
        for month in range(1, 12, month_interval):
            start_date = date(year, month, period_start)
            if month + month_interval > 12:
                year += 1
                month = 1
                end_date = date(year, month, period_start)
            else:
                end_date = date(year, month+month_interval, period_start)
            e, i = calc_period(start_date, end_date)
            result.append((start_date, end_date, e, i))
    return result

