import csv
import optparse
from datetime import date

from admin.Init import load_from_csv, create_new_database
import analytics.Summation


def f2s(f):
    return '%10.2f' % f

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file", help="CSV input file", dest="csv_data_in")
    parser.add_option("-i", "--initialize", help="create new database", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.initialize is True:
        create_new_database()
    if options.csv_data_in is not None:
        csv_data_in = options.csv_data_in
        with open(csv_data_in, newline='', encoding='ansi') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            load_from_csv(csv_reader)
    s = analytics.Summation.Summation()
    ytd = 0.0
    for i in range(1,13,1):
        m = s.sum_month(2017, i)
        ytd += m
        print('%2d' % i, f2s(m), f2s(ytd))
    print(f2s(s.sum_year(2017)))
    all_sum = 0
    for y in range(2011, 2018, 1):
        year_sum = s.sum_year(y)
        all_sum += year_sum
        print(y, f2s(year_sum), f2s(all_sum))