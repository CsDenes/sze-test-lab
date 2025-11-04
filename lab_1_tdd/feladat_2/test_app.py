import os
import tempfile
import pytest
from feladat_2.app import app, init_db

@pytest.fixture
def client():
    """
    Test client fixture. This sets up a temporary database for testing
    and yields a Flask test client.
    """
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    app.config.update({
        "TESTING": True,
        "DATABASE": db_path,
    })

    # Initialize the database with the schema
    with app.app_context():
        init_db()

    # Yield the test client
    with app.test_client() as client:
        yield client

    # Clean up by closing the file and removing it
    os.close(db_fd)
    os.unlink(db_path)

def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_get_empty_todos(client):
    """Test GET /todos when the database is empty."""
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json == []

def test_create_todo(client):
    """Test creating a new to-do item via POST /todos."""
    # Create a new todo
    response = client.post('/todos', json={'task': 'My first test todo'})
    assert response.status_code == 201
    
    # Verify it was added by getting all todos
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['task'] == 'My first test todo'
