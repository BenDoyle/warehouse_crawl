import os
import pytest

@pytest.fixture
def altars_path():
    return os.path.join(os.path.dirname(__file__), 'fixtures', 'altars', 'altars.csv')

@pytest.fixture
def altars_schema_path():
    return os.path.join(os.path.dirname(__file__), 'fixtures', 'altars', 'altars.schema.json')