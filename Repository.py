import sqlite3
import uuid


db_file = 'db.sqlite3'

class TransferRepository:
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
    def add(self, transfer_entry):
        account_number = transfer_entry.acc_number()
        acc_oid = ''
        try:
            acc_oid = self.insert_account(account_number)
        except Exception as ex:
            print(ex, flush=True)
            acc_oid = self.select_account_oid(account_number)
        try:
            date = transfer_entry.date()
            amount = transfer_entry.amount()
            type = transfer_entry.type()
            title = transfer_entry.title()
            saldo = transfer_entry.saldo_after_transaction()
            tr_oid = self.insert_transaction(acc_oid, date, amount, saldo, type, title)
        except Exception as ex:
            print(ex, flush=True)
            self.conn.rollback()
        self.conn.commit()

    def insert_account(self, account_number):
        if not account_number.isdigit():
            raise Exception("Bad account number `%s'"%(account_number))
        oid = uuid.uuid4().hex
        query = '''INSERT INTO account_numbers(oid, number) VALUES(?,?)'''
        self.cur.execute(query, [oid, account_number])
        return oid
    def select_account_oid(self, account_number):
        query = '''SELECT oid FROM account_numbers WHERE number = ?'''
        self.cur.execute(query, [account_number])
        row = self.cur.fetchone()
        return row[0]
    def insert_transaction(self, acc_oid, date, amount, saldo_after_tr, type, title):
        query = '''select oid from transactions where tr_date = ? and amount = ? and saldo_after_tr = ?'''
        self.cur.execute(query, (date, amount, saldo_after_tr))
        r = self.cur.fetchall()
        if len(r) > 0:
            raise Exception("Double insert     e r r o r")
        tr_oid = uuid.uuid4().hex
        query = '''INSERT INTO transactions(oid,tr_date,amount,saldo_after_tr) VALUES(?,?,?,?)'''
        self.cur.execute(query, (tr_oid, date, amount, saldo_after_tr))
        query = '''INSERT INTO transaction_details(tr_oid,type,title) VALUES(?,?,?)'''
        self.cur.execute(query, (tr_oid, type, title))
        query = '''INSERT INTO transfer_log(tr_oid,acc_oid) VALUES(?,?)'''
        self.cur.execute(query, (tr_oid, acc_oid))
        return tr_oid

class BaseRepository:
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
    def add(self, cart_entry):
        try:
            tr_oid = self.insert_transaction(cart_entry)
        except Exception as ex:
            print(ex, flush=True)
            self.conn.rollback()
        self.conn.commit()
    def prevent_double_insert(self, e):
        query = '''select oid from transactions where tr_date = ? and amount = ? and saldo_after_tr = ?'''
        self.cur.execute(query, (e.date(), e.amount(), e.saldo_after_transaction()))
        r = self.cur.fetchall()
        if len(r) > 0:
            raise Exception("Double insert     e r r o r")
    def extract_date_from_title(self, e):
        str = 'DATA TRANSAKCJI: '
        title = e.title()
        idx = title.find(str)
        if idx == -1:
            return e.date(), e.title()
        tr_date = title[idx+len(str):].strip('" ')
        return tr_date, title[:idx].strip()
    def insert_transaction(self, e):
        self.prevent_double_insert(e)
        tr_oid = uuid.uuid4().hex
        query = '''INSERT INTO transactions(oid,tr_date,amount,saldo_after_tr) VALUES(?,?,?,?)'''
        self.cur.execute(query, (tr_oid, e.date(), e.amount(), e.saldo_after_transaction()))
        tr_date, base_title = self.extract_date_from_title(e)
        query = '''INSERT INTO transaction_details(tr_oid,type,title,tr_date) VALUES(?,?,?,?)'''
        self.cur.execute(query, (tr_oid, e.type(), base_title, tr_date))
        return tr_oid


class CartTransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    

class AtmRepository(BaseRepository):
    def __init__(self):
        super().__init__()