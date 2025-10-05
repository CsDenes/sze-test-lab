import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json

# Make the Flask app and its in-memory data store accessible to the tests
from lab_2_bdd.app import app, todos

# Constants
EXISTING_TODO = {"id": 2, "task": "Build a Flask API", "done": True}

# Scenarios
scenarios('./features/single_todo.feature')

# Fixtures
@pytest.fixture
def client():
    """Provides a test client for the Flask application."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def response(client):
    """A fixture to store the response from an API call."""
    return {}
