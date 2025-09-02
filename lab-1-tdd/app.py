from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the To-Do API!"

# In-memory data store
todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]