import os
import sqlite3
import json
import csv

def load(database, table_name, csv_path, force):
    database = os.path.abspath(database)
    csv_path = os.path.abspath(csv_path)

    def load_database():
        assert not os.path.isdir(database), 'The database argument cannot be a directory'
        dirname = os.path.dirname(database)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return sqlite3.connect(database)

    def load_schema():
        schema_path = os.path.join(csv_path, '.schema')
        assert os.path.exists(schema_path), 'Schema not found: {}'.format(schema_path)
        with open(schema_path, 'r') as fd:
            return json.load(fd)

    def create_table(db, schema):

        existing_table = db.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{}';".format(table_name)).fetchone()
        if existing_table:
            return

        schema = load_schema()
        create_table = (
            'CREATE TABLE {} ('.format(table_name) +
            ', '.join('{} {}'.format(name_, type_) for name_, type_ in schema.items()) +
            ')'
        )
        db.execute(create_table)

    def load_csv_from_path(db, schema):
        assert os.path.exists(csv_path), 'CSV path does not exist: {}'.format(csv_path)

        def load_csv_values(path):
            with open(path, 'r') as fd:
                reader = csv.reader(fd)
                for row in reader:
                    yield row

        def escape_value(value, type_):
            return {
                'TEXT':     lambda v: '"{}"'.format(v.replace('"', '\"')),
                'REAL':     lambda v: str(float(v)),
                'INTEGER':  lambda v: str(int(v)),
            }.get(type_.upper())(value)

        def insert_row(row, cursor):
            escaped_rows = [(col_name, escape_value(value, col_type)) for (value, (col_name, col_type)) in zip(row, schema.items())]
            col_names, values = zip(*escaped_rows)
            sql = 'INSERT INTO {table_name} ({col_names}) VALUES ({values})'.format(
                table_name=table_name,
                col_names=', '.join(col_names),
                values=', '.join(values)
            )
            cursor.execute(sql)

        for file_ in os.listdir(csv_path):
            if not file_.endswith('.csv'):
                continue
            cursor = db.cursor()
            for row in load_csv_values(os.path.join(csv_path, file_)):
                insert_row(row, cursor)
            cursor.close()
            
    schema = load_schema()
    db = load_database()
    create_table(db, schema)
    load_csv_from_path(db, schema)
    db.commit()
    db.close()

if __name__ == '__main__':
    options = ['database', 'table_name', 'csv_path', 'force']
    required = ['database', 'table_name', 'csv_path']

    env = {
        option: os.environ.get(option.upper())
        for option in options
    }
    missing_options = set(required) & set(option for option, value in env.items() if not value)
    if set(required) & set(option for option, value in env.items() if not value):
        raise Exception('Missing required options: {}'.format(missing_options))

    load(**env)
