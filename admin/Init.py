import sqlite3
import Entry
import uuid
import os

db_file = 'db.sqlite3'

class Init(object):
    @staticmethod
    def create_database():
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE trans_desc_orig(id integer, desc text)''')
        cur.execute('''CREATE UNIQUE INDEX trans_desc_id_idx ON trans_desc_orig(id)''')
        cur.execute('''CREATE TABLE account_numbers(oid text, number text)''')
        cur.execute('''CREATE UNIQUE INDEX account_numbers_oid_idx ON account_numbers(oid)''')
        cur.execute('''CREATE UNIQUE INDEX account_numbers_number_idx ON account_numbers(number)''')
        cur.execute('''CREATE TABLE transactions(oid text, tr_date date, amount real, saldo_after_tr real)''')
        cur.execute('''CREATE TABLE transaction_details(tr_oid text, type text, title text, tr_date date)''')
        cur.execute('''CREATE TABLE transfer_log(tr_oid text, acc_oid text)''')


def create_new_database():
    if os.path.isfile(db_file):
        os.remove(db_file)
        print("Removed: " + db_file, flush=True)
    Init().create_database()


def load_account_numbers(csv_reader):
    for r in csv_reader:
        if len(r) == 9:
            try:
                e = Entry.create(r)
                e.from_csv(r)
                repository = e.repository()
                repository.add(e)
            except Exception as ex:
                print(ex, flush=True)


if __name__ == '__main__':
    create_new_database()
