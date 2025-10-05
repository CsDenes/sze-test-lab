from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store
todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]

@app.route('/')
def index():
    return "Welcome"

@app.route('/todos', methods=['GET', 'POST'])
def get_todos():
    if request.method == 'GET':
        return jsonify(todos)
    elif request.method == 'POST':
        new_todo = {
            'id': max(todo['id'] for todo in todos) + 1 if todos else 1,
            'task': request.json['task'],
            'done': False  # New tasks are not done by default
        }
        todos.append(new_todo)
        return jsonify(new_todo), 201
