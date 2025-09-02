import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    """Test the root endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the To-Do API!" in response.data