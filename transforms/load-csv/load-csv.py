import os
import simplejson as json
import csv

from postgres_loader import PostgresLoader
from sqlite_loader import SqliteLoader

class PostgresCsvDialect(csv.Dialect):
    delimiter = '~'
    quoting = csv.QUOTE_MINIMAL
    quotechar = '"'
    lineterminator = '\n'

def load_schema(path):
    path = os.path.abspath(path)
    assert os.path.exists(path), 'Schema not found: {}'.format(path)
    with open(path, 'r') as fd:
        return json.load(fd)

def load_csv_rows(path):
    path = os.path.abspath(path)
    assert os.path.exists(path), 'CSV path does not exist: {}'.format(path)
    with open(path, 'r') as fd:
        reader = csv.reader(fd, dialect=PostgresCsvDialect())
        for row in reader:
            yield row

def get_loader(type_, **configuration):
    LOADERS = {
        'postgres': PostgresLoader,
        'sqlite': SqliteLoader
    }
    assert type_ in LOADERS, 'Invalid loader type: {}, expected one of {}'.format(type_, LOADERS.keys())
    return LOADERS.get(type_)(**configuration)

def load(db_type, table_name, csv_path, schema, configuration):
    with get_loader(db_type, **configuration) as loader:
        if loader.table_exists(table_name):
            loader.drop_table(table_name)
        loader.create_table(table_name, schema)

        for row in load_csv_rows(csv_path):
            loader.insert_row(table_name, schema, row)

if __name__ == '__main__':
    options = ['type', 'configuration', 'table_name', 'csv_path', 'schema_path']
    required = options

    env = {
        option: os.environ.get(option.upper())
        for option in options
    }
    missing_options = set(required) & set(option for option, value in env.items() if not value)
    if set(required) & set(option for option, value in env.items() if not value):
        raise Exception('Missing required options: {}'.format(missing_options))

    schema = load_schema(env['schema_path'])
    with open(env['configuration']) as fd:
        configuration = json.load(fd)

    load(env['type'], env['table_name'], env['csv_path'], schema, configuration)
