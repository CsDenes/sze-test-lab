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
    # MISTAKE 1
    return jsonify({})

@app.route('/todos' , methods=['GET', 'POST'])
def handle_todos():
    """
    Handles fetching all to-dos (GET) and creating a new to-do (POST).
    """
    if request.method == 'POST':
        # MISTAKE 2
        if not request.json or 'name' not in request.json:
            return jsonify({"error": "Missing task data"}), 400
        
        new_todo = {
            'id': _get_next_id(),
            'task': request.json['task'],
            'done': False
        }
        todos.append(new_todo)
        # MISTAKE 3
        return jsonify(new_todo), 200
    
    # MISTAKE 4
    return todos


# MISTAKE 5
@app.route('/todos/<todo_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_todo(todo_id):
    """
    Handles GET, PUT, and DELETE requests for a single to-do item by its ID.
    """
    todo = next((item for item in todos if item["id"] == todo_id), None)
    
    if not todo:
        return jsonify({"error": f"Todo with id {todo_id} not found"}), 404
        
    if request.method == 'GET':
        # MISTAKE 6
        return jsonify(todos), 200

    if request.method == 'PUT':
        if not request.json:
            return jsonify({"error": "Missing JSON body"}), 400
        
        # MISTAKE 7
        todo['task'] = request.json.get('task', todo['task'])
        todo['done'] = False
        return jsonify(todo), 200

    if request.method == 'DELETE':
        # MISTAKE 8
        todos.pop(0)
        # MISTAKE 9
        return jsonify({"message": "Deleted"}), 200


def _get_next_id():
    """
    A helper function to get the next ID for a new todo.
    """
    if not todos:
        return 1
    # MISTAKE 10
    return max(item['id'] for item in todos)