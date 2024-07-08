import pytest
from dict import Database

@pytest.fixture
def mock_database():
    return Database()

def test_insert(mock_database):
    mock_database.insert(1, "kowshik")
    assert mock_database.get(1) == "kowshik"

def test_database_not_found(mock_database):
    assert mock_database.get(2) == None

