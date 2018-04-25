import uuid
import Entry
import Database


class Criteria(object):
    pass


class Repository(object):
    def __init__(self, **kwargs):
        self.db = Database.database_factory()
        return super().__init__(**kwargs)
    def find(self, begin, end):
        query = '''select t.oid,t.tr_date,td.tr_date,td.type,td.title,ifnull(an.number, null),t.amount,t.saldo_after_tr from transactions t join transaction_details td on t.oid=td.tr_oid left join transfer_log tl on t.oid=tl.tr_oid left join account_numbers an on tl.acc_oid=an.oid where t.tr_date >= ? and t.tr_date <= ? order by t.tr_date'''
        stmt = self.db.statement(query)
        stmt.execute((begin, end))
        return self._get_entries(stmt)
    def find_transfer(self, begin, end, account_number):
        query = '''select t.oid,t.tr_date,td.tr_date,td.type,td.title,ifnull(an.number, null),t.amount,t.saldo_after_tr from transactions t join transaction_details td on t.oid=td.tr_oid left join transfer_log tl on t.oid=tl.tr_oid left join account_numbers an on tl.acc_oid=an.oid where t.tr_date >= ? and t.tr_date <= ? and an.number = ? order by t.tr_date'''
        stmt = self.db.statement(query)
        stmt.execute((begin, end, account_number))
        return self._get_entries(stmt)
    def find_by_criteria(self, a_criteria):
        pass
    def _get_entries(self, stmt):
        entries = []
        row = stmt.next()
        while row is not None:
            e = Entry.Entry()
            r = [row.get_string(), row.get_date(), row.get_date(), row.get_string(), row.get_string(),
                 row.get_string(), row.get_float(), row.get_float()]
            e.from_db(r)
            entries.append(e)
            row = stmt.next()
        return entries


class TransferRepository:
    def __init__(self):
        self.db = Database.database_factory()
    def add(self, transfer_entry):
        account_number = transfer_entry.acc_number()
        acc_oid = ''
        try:
            acc_oid = self.insert_account(account_number)
        except Exception as ex:
            # print(ex, flush=True)
            acc_oid = self.select_account_oid(account_number)
        try:
            date = transfer_entry.date()
            amount = transfer_entry.amount()
            type = transfer_entry.type()
            title = transfer_entry.title()
            saldo = transfer_entry.saldo_after_transaction()
            tr_oid = self.insert_transaction(acc_oid, date, amount, saldo, type, title)
        except Exception as ex:
            # print(ex, flush=True)
            self.db.rollback()
        self.db.commit()

    def insert_account(self, account_number):
        if not account_number.isdigit():
            raise Exception("Bad account number `%s'"%(account_number))
        oid = uuid.uuid4().hex
        query = '''INSERT INTO account_numbers(oid, number) VALUES(?,?)'''
        stmt = self.db.statement(query)
        stmt.execute((oid, account_number))
        row = stmt.next()
        return oid
    def select_account_oid(self, account_number):
        query = '''SELECT oid FROM account_numbers WHERE number = ?'''
        stmt = self.db.statement(query)
        stmt.execute([account_number])
        row = stmt.next()
        return row.get_string()
    def insert_transaction(self, acc_oid, date, amount, saldo_after_tr, type, title):
        query = '''select oid from transactions where tr_date = ? and amount = ? and saldo_after_tr = ?'''
        stmt = self.db.statement(query)
        stmt.execute((date, amount, saldo_after_tr))
        r = stmt.next()
        if r is not None:
            raise Exception("Double insert     e r r o r")
        tr_oid = uuid.uuid4().hex
        query = '''INSERT INTO transactions(oid,tr_date,amount,saldo_after_tr) VALUES(?,?,?,?)'''
        stmt = self.db.statement(query)
        stmt.execute((tr_oid, date, amount, saldo_after_tr))
        query = '''INSERT INTO transaction_details(tr_oid,type,title) VALUES(?,?,?)'''
        stmt = self.db.statement(query)
        stmt.execute((tr_oid, type, title))
        query = '''INSERT INTO transfer_log(tr_oid,acc_oid) VALUES(?,?)'''
        stmt = self.db.statement(query)
        stmt.execute((tr_oid, acc_oid))
        return tr_oid

class BaseRepository:
    def __init__(self):
        self.db = Database.database_factory()
    def add(self, cart_entry):
        try:
            tr_oid = self.insert_transaction(cart_entry)
        except Exception as ex:
            # print(ex, flush=True)
            self.db.rollback()
        self.db.commit()
    def prevent_double_insert(self, e):
        query = '''select oid from transactions where tr_date = ? and amount = ? and saldo_after_tr = ?'''
        stmt = self.db.statement(query)
        stmt.execute((e.date(), e.amount(), e.saldo_after_transaction()))
        r = stmt.next()
        if r is not None:
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
        stmt = self.db.statement(query)
        stmt.execute((tr_oid, e.date(), e.amount(), e.saldo_after_transaction()))
        tr_date, base_title = self.extract_date_from_title(e)
        query = '''INSERT INTO transaction_details(tr_oid,type,title,tr_date) VALUES(?,?,?,?)'''
        stmt = self.db.statement(query)
        stmt.execute((tr_oid, e.type(), base_title, tr_date))
        return tr_oid


class CartTransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    

class AtmRepository(BaseRepository):
    def __init__(self):
        super().__init__()