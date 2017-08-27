import os
import glob
import csv

import Entry
import Database


class Init(object):
    def __init__(self):
        self.create_sql_file = 'admin\\create.sql'
    def load_creation_script(self):
        with open(self.create_sql_file) as file:
            return file.read()
    def create_db(self):
        database = Database.database_factory()
        stmt = database.statement('')
        stmt.executescript(self.load_creation_script())


def create_new_database():
    db_file = Database.db_file
    if os.path.isfile(db_file):
        os.remove(db_file)
        print("Removed: " + db_file, flush=True)
    Init().create_db()

def load_data_from_files(pattern):
    for file in glob.glob(os.path.join('', pattern)):
        with open(file, newline='', encoding='ansi') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';', quotechar='"')
            load_from_csv(csv_reader)

def load_from_csv(csv_reader):
    for line in csv_reader:
        if len(line) == 9:
            if line[6] == '#Saldo końcowe':
                continue
            try:
                entry = Entry.create_from_csv(line)
                repository = entry.repository()
                repository.add(entry)
            except Exception as ex:
                if str(ex) == 'MetaRepository not implemented':
                    pass
                else:
                    raise ex


if __name__ == '__main__':
    create_new_database()
