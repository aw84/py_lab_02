import Entry
import uuid
import os
import Database


db_file = 'db.sqlite3'

class Init(object):
    @staticmethod
    def create_database():
        db = Database.Database(db_file)
        s = db.statement('''CREATE TABLE account_numbers(oid text, number text)''')
        s.execute()
        s = db.statement('''CREATE UNIQUE INDEX account_numbers_oid_idx ON account_numbers(oid)''')
        s.execute()
        s = db.statement('''CREATE UNIQUE INDEX account_numbers_number_idx ON account_numbers(number)''')
        s.execute()
        s = db.statement('''CREATE TABLE transactions(oid text, tr_date date, amount real, saldo_after_tr real)''')
        s.execute()
        s = db.statement('''CREATE UNIQUE INDEX transactions_oid_idx ON transactions(oid)''')
        s.execute()
        s = db.statement('''CREATE INDEX transactions_tr_date_idx ON transactions(tr_date)''')
        s.execute()
        s = db.statement('''CREATE INDEX transactions_amount_idx ON transactions(amount)''')
        s.execute()
        s = db.statement('''CREATE INDEX transactions_saldo_after_tr_idx ON transactions(saldo_after_tr)''')
        s.execute()
        s = db.statement('''CREATE TABLE transaction_details(tr_oid text, type text, title text, tr_date date)''')
        s.execute()
        s = db.statement('''CREATE UNIQUE INDEX transaction_details_tr_oid_idx ON transaction_details(tr_oid)''')
        s.execute()
        s = db.statement('''CREATE TABLE transfer_log(tr_oid text, acc_oid text)''')
        s.execute()


def create_new_database():
    if os.path.isfile(db_file):
        os.remove(db_file)
        print("Removed: " + db_file, flush=True)
    Init().create_database()


def load_from_csv(csv_reader):
    for r in csv_reader:
        if len(r) == 9:
            if r[6] == '#Saldo końcowe':
                continue
            try:
                e = Entry.create_from_csv(r)
                repository = e.repository()
                repository.add(e)
            except Exception as ex:
                print(ex, flush=True)
                if str(ex) == 'MetaRepository not implemented':
                    pass
                else:
                    raise ex


if __name__ == '__main__':
    create_new_database()
