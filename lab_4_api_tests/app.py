from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]

@app.route('/')
def index():
    """
    Welcome endpoint.
    """
    return "Welcome"

@app.route('/todos' , methods=['GET', 'POST'])
def handle_todos():
    """
    Handles fetching all to-dos (GET) and creating a new to-do (POST).
    """
    if request.method == 'POST':
        # Validate that the request has JSON and contains a 'task' field
        if not request.json or 'task' not in request.json:
            return jsonify({"error": "Missing task data"}), 400
        
        new_todo = {
            'id': _get_next_id(),
            'task': request.json['task'],
            'done': False  # New tasks are not done by default
        }
        todos.append(new_todo)
        return jsonify(new_todo), 201
    
    # This handles the GET request
    return jsonify(todos)


@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_todo(todo_id):
    """
    Handles GET, PUT, and DELETE requests for a single to-do item by its ID.
    """
    # Find the todo with the matching ID
    todo = next((item for item in todos if item["id"] == todo_id), None)
    
    # If the todo doesn't exist, return 404 for any method
    if not todo:
        return jsonify({"error": f"Todo with id {todo_id} not found"}), 404
        
    if request.method == 'GET':
        # If found, return the todo item with a 200 OK status
        return jsonify(todo), 200

    if request.method == 'PUT':
        # Validate that the request contains a JSON body
        if not request.json:
            return jsonify({"error": "Missing JSON body"}), 400
        
        # Use dict.update() to apply all changes from the request body.
        # This correctly handles updating 'task', 'done', or both.
        todo.update(request.json)
        return jsonify(todo), 200

    if request.method == 'DELETE':
        # If found, remove it from the list
        todos.remove(todo)
        # Return an empty response with a 204 No Content status
        return '', 204


def _get_next_id():
    """
    A helper function to get the next ID for a new todo.
    """
    # If the list is empty, start with ID 1. Otherwise, find the max ID and add 1.
    if not todos:
        return 1
    return max(item['id'] for item in todos) + 1
