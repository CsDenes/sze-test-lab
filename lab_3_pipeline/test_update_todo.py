import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import json

# Make the Flask app and its in-memory data store accessible to the tests
# Adjust the import path based on your project structure
from lab_3_pipeline.app import app, todos

# Scenarios
scenarios('./features/update_todo.feature')

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

# --- NEW STEP TO PREPARE THE PAYLOAD ---
@given(parsers.parse('the user has prepared an update payload with task "{task}" and done status "{done_status}"'), target_fixture="update_payload")
def prepare_update_payload(task, done_status):
    """
    Creates a dictionary payload and stores it in the 'update_payload' fixture.
    Converts string 'true'/'false' to boolean.
    """
    # json.loads is a reliable way to convert 'true'/'false' strings to booleans
    done = json.loads(done_status.lower())
    return {"task": task, "done": done}

# Given Steps
@given('the API has a to-do with id 1 and task "Learn TDD"')
def setup_specific_todo():
    """Set up the initial state with a to-do that can be updated."""
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
    ]

@given('the API has a list of to-dos')
def setup_any_todos():
    """Set up the initial state with a generic list."""
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
    ]

@when(parsers.parse('the user sends a PUT request to update the to-do with id {todo_id}'))
def send_update_request(client, response, todo_id, update_payload):
    """
    Make a PUT request to the /todos/<id> endpoint, using the payload
    from the 'update_payload' fixture.
    """
    res = client.put(f'/todos/{todo_id}', json=update_payload)
    response['status_code'] = res.status_code
    if res.content_type == 'application/json':
        response['data'] = res.get_json()

# Then Steps
@then(parsers.parse('the response status code should be {status_code:d}'))
def check_status_code(response, status_code):
    """Check if the response status code is the expected one."""
    assert response['status_code'] == status_code

@then(parsers.parse('the response should contain the updated to-do with id {todo_id:d}, task "{task}", and done status "{done_status}"'))
def check_response_for_updated_todo(response, todo_id, task, done_status):
    """Check the content of the response for a successful update."""
    done = json.loads(done_status.lower())
    expected_data = {
        "id": todo_id,
        "task": task,
        "done": done
    }
    assert response['data'] == expected_data

@then(parsers.parse('the to-do with id {todo_id:d} in the list should be fully updated with task "{task}" and done status "{done_status}"'))
def check_in_memory_list_is_updated(todo_id, task, done_status):
    """Check that the actual in-memory list reflects the full update."""
    done = json.loads(done_status.lower())
    todo_in_list = next((item for item in todos if item["id"] == int(todo_id)), None)
    assert todo_in_list is not None
    assert todo_in_list['task'] == task
    assert todo_in_list['done'] is done

@then('the response should contain a "not found" error message')
def check_response_for_not_found(response):
    """Check the content of the response for a 404 error."""
    assert 'error' in response['data']
    assert 'not found' in response['data']['error'].lower()