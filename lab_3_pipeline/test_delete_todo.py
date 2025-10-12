import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json

# Make the Flask app and its in-memory data store accessible to the tests
from lab_3_pipeline.app import app, todos

# Scenarios
scenarios('./features/delete_todo.feature')

# Fixtures
@pytest.fixture
def client():
    """Provides a test client for the Flask application."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def response():
    """A fixture to store the response from an API call."""
    return {}

# One of the benefits of BDD is reusing steps. pytest-bdd will automatically find
# the 'given' steps we already wrote in `test_single_todo.py`. However, for
# clarity and to test the "unchanged list" scenario, we'll define them here
# using a target_fixture to save the initial state.

@given('the API has a to-do with id 1 and task "Learn TDD"', target_fixture="initial_state")
def setup_specific_todo():
    """Set up the initial state with a to-do that can be deleted."""
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
    ]
    return list(todos) # Return a copy of the initial state

@given('the API has a list of to-dos', target_fixture="initial_state")
def setup_any_todos():
    """Set up the initial state with a generic list."""
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
    ]
    return list(todos) # Return a copy of the initial state

# When Steps
@when(parsers.parse('the user sends a DELETE request for the to-do with id {todo_id}'))
def delete_single_todo(client, response, todo_id):
    """Make a DELETE request to the /todos/<id> endpoint."""
    res = client.delete(f'/todos/{todo_id}')
    response['status_code'] = res.status_code
    # Note: A 204 response has no JSON body to parse

# Then Steps
@then(parsers.parse('the response status code should be {status_code:d}'))
def check_status_code(response, status_code):
    """Check if the response status code is the expected one."""
    assert response['status_code'] == status_code

@then(parsers.parse('the to-do with id {todo_id:d} should no longer be in the list'))
def check_todo_is_removed(todo_id):
    """Check that the to-do has been removed from the in-memory list."""
    ids_in_list = [item['id'] for item in todos]
    assert todo_id not in ids_in_list

@then('the list of to-dos should be unchanged')
def check_list_is_unchanged(initial_state):
    """Check that the list was not modified after a failed delete attempt."""
    assert todos == initial_state