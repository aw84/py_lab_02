from datetime import date
import csv
import argparse

import Command
import settings

from admin.Init import load_from_csv, create_new_database, load_data_from_files
import analytics.Summation
import analytics.Category
from analytics import calcpack
from settings import f2s


def list_entries(date_begin, date_end):
    ts = analytics.Summation.TransactionService()
    entries = ts.find(settings.create_date(date_begin), settings.create_date(date_end))
    for e in entries:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="CSV input file", dest="csv_data_in")
    parser.add_argument("-p", "--file-pattern", help="CSV input files pattern",
                        dest="csv_file_pattern")
    parser.add_argument("-i", "--initialize", help="create new database", action="store_true",
                        default=False)
    parser.add_argument("-c", "--command", help="Use command syntax to list entries", dest="command_string")
    options = parser.parse_args()
    if options.initialize is True:
        create_new_database()
    if options.csv_file_pattern is not None and options.csv_data_in is not None:
        print("Choose -f or -p, not both of them")
        exit(0)
    if options.csv_data_in is not None:
        csv_data_in = options.csv_data_in
        with open(csv_data_in, newline='', encoding='ansi') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            load_from_csv(csv_reader)
    if options.csv_file_pattern is not None:
        load_data_from_files(options.csv_file_pattern)
    if options.command_string is not None:
        cmd = Command.Command.create(options.command_string)
        [print(i) for i in cmd.run()]
        exit(0)

    list_entries('2018-01-01', '2018-05-01')
    # exit(0)
    year_begin = 2018
    year_end = 2019
    month_interval = 3
    result = calcpack.calculate_interval(year_begin, year_end, month_interval)
    for r in result:
        try: 
            print("[", r[0], r[1], ")", flush=True)
        except:
            print("error", flush=True)
        print("Expences: ", r[2], flush=True)
        try:
            print("Income:   ", r[3], flush=True)
        except:
            print("error", flush=True)
    ts = analytics.Summation.TransactionService()
    entries = ts.find(date(year_begin, 1, 1), date(year_end, 1, 1))
    salary = []
    expences = []
    for e in entries:
        if e.amount() > 0:
            salary.append(e.amount())
        else:
            expences.append(e.amount())
    cp = calcpack.CalcPack(salary)
    salary_sum = cp.sum()
    cp = calcpack.CalcPack(expences)
    expences_sum = cp.sum()
    print("Salary on [%d, %d):   " % (year_begin, year_end), f2s(salary_sum))
    print("Expences on [%d, %d): " % (year_begin, year_end), f2s(expences_sum))
    print("Diff on [%d, %d):     " % (year_begin, year_end), f2s(salary_sum + expences_sum))

    s = analytics.Summation.Summation()
    for y in range(year_begin-1, year_end, 1):
        year_sum = s.sum_year(y)
        print(y, f2s(year_sum), f2s(s.sum_year_transfer_amount(y, '57105015041000002310394032')))

    entries = ts.find(date(year_begin, 1, 1), date(year_end, 1, 1))
    xxx = 0
    cnt = 0
    for e in entries:
        c = analytics.Category.Category()
        cat_id = c.guess(e)
        if cat_id == analytics.Category.CategoryId(analytics.Category.CategoryId.id_6):
            xxx += e.amount()
            cnt += 1
            print(e.date(), f2s(e.amount()), f2s(xxx), c.description(cat_id), flush=True)
    data = {
        0 : [], -100 : [], -300 : [], -600 : [], -900 : []
    }
    entries = ts.find(date(year_begin, 1, 1), date(year_end, 1, 1))
    saldo = 0
    for e in entries:
        if e.amount() > 5000:
            print(e.date(), f2s(e.amount()), f2s(e.saldo_after_transaction()),
                  f2s(e.saldo_after_transaction() - saldo), flush=True)
            saldo = e.saldo_after_transaction()
    entries = ts.find(date(year_begin, 1, 1), date(year_end, 1, 1))
    exp = 0
    for e in entries:
        amt = e.amount()
        c = analytics.Category.Category()
        cat_id = c.guess(e)
        if cat_id is None:
            if amt < 0 and  amt >= -100:
                data[0].append(amt)
            elif amt < -100 and  amt >= -300:
                data[-100].append(amt)
            elif amt < -300 and  amt >= -600:
                data[-300].append(amt)
            elif amt < -600 and  amt >= -900:
                data[-600].append(amt)
            elif amt < -900:
                data[-900].append(amt)
    for k in data:
        cp = calcpack.CalcPack(data[k])
        if len(data[k]) > 0:
            print("%4d" % k, cp)