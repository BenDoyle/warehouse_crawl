import mock
import pytest

import os

from postgres_loader import PostgresLoader

@pytest.fixture
def loader():
    with mock.patch('postgres_loader.connect_postgres', mock.Mock(name='mock postres connection')):
        yield PostgresLoader('dbconnection')

def test_run(loader, altars_path, altars_schema_path):
    loader.run('altars', altars_path, altars_schema_path)
    assert False, 'TODO'
