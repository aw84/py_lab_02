import csv
import optparse

from admin.Init import load_account_numbers, create_new_database


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
            load_account_numbers(csv_reader)
