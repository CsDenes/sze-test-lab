from flask import Flask, jsonify, request
# Opcionális, de ajánlott, ha böngészőből tesztelsz, a CORS hibák elkerülésére
# Telepítés: pip install flask-cors
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Engedélyezi a cross-origin kéréseket minden domainről

# Memóriában tárolt adatok (In-memory data store)
todos = [
    {"id": 1, "task": "Learn TDD", "done": False},
    {"id": 2, "task": "Build a Flask API", "done": True},
]

def _get_next_id():
    """
    Segédfüggvény a következő ID generálásához.
    """
    if not todos:
        return 1
    return max(item['id'] for item in todos) + 1

@app.route('/')
def index():
    """
    Üdvözlő végpont.
    """
    return "Welcome to the To-Do API. Használd a /todos végpontot."

@app.route('/todos' , methods=['GET', 'POST'])
def handle_todos():
    """
    Kezeli az összes teendő lekérését (GET) és új teendő létrehozását (POST).
    """
    if request.method == 'POST':
        # Validáció: van-e JSON és 'task' mező
        if not request.json or 'task' not in request.json:
            return jsonify({"error": "Missing task data"}), 400
        
        new_todo = {
            'id': _get_next_id(),
            'task': request.json['task'],
            'done': False  # Alapértelmezetten nincs kész
        }
        todos.append(new_todo)
        return jsonify(new_todo), 201
    
    # GET kérés kezelése
    return jsonify(todos)


@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_todo(todo_id):
    """
    Kezeli az egyedi teendőre vonatkozó GET, PUT, DELETE kéréseket ID alapján.
    """
    # Keresd meg a teendőt
    todo = next((item for item in todos if item["id"] == todo_id), None)
    
    # Ha nincs meg, 404
    if not todo:
        return jsonify({"error": f"Todo with id {todo_id} not found"}), 404
        
    if request.method == 'GET':
        return jsonify(todo), 200

    if request.method == 'PUT':
        # Validáció: van-e JSON törzs
        if not request.json:
            return jsonify({"error": "Missing JSON body"}), 400
        
        # Frissíti a 'task' és/vagy 'done' mezőket
        todo.update(request.json)
        return jsonify(todo), 200

    if request.method == 'DELETE':
        todos.remove(todo)
        # 204 No Content: Sikeres törlés, nincs visszatérési törzs
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)