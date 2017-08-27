CREATE TABLE account_numbers(oid text, number text);
CREATE TABLE transactions(oid text, tr_date date, amount real, saldo_after_tr real);
CREATE TABLE transaction_details(tr_oid text, type text, title text, tr_date date);
CREATE TABLE transfer_log(tr_oid text, acc_oid text);
CREATE TABLE categories(oid text, cname text);
CREATE TABLE transaction_category(tr_oid, cat_oid);

CREATE UNIQUE INDEX account_numbers_oid_idx ON account_numbers(oid);
CREATE UNIQUE INDEX account_numbers_number_idx ON account_numbers(number);

CREATE UNIQUE INDEX transactions_oid_idx ON transactions(oid);
CREATE INDEX transactions_tr_date_idx ON transactions(tr_date);
CREATE INDEX transactions_amount_idx ON transactions(amount);
CREATE INDEX transactions_saldo_after_tr_idx ON transactions(saldo_after_tr);

CREATE UNIQUE INDEX transaction_details_tr_oid_idx ON transaction_details(tr_oid);

CREATE UNIQUE INDEX categories_oid_idx ON categories(oid);
CREATE UNIQUE INDEX categories_cname_idx ON categories(cname);

CREATE UNIQUE INDEX transaction_category_tr_oid_idx ON transaction_category(tr_oid);
CREATE INDEX transaction_category_cat_oid_idx ON transaction_category(cat_oid);
