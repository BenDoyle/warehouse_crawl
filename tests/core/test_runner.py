import pytest
from core import runner

@pytest.fixture
def processors_repo_path():
    return None

def test_discover_processors(processors_repo_path):
    processors = runner.discover_processors(processors_repo_path)
    assert False, 'TODO'