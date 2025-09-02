# **Lab Exercise: Test-Driven Development with Python and Flask**

Objective:  
The goal of this exercise is to provide hands-on experience with the Test-Driven Development (TDD) methodology. You will build a simple To-Do List REST API using the Flask framework. By following the TDD workflow, you will write tests before writing the application code, ensuring that your application is well-tested and that its development is guided by a clear set of requirements.  
**Prerequisites:**

* Python 3.6+ installed.  
* pip package manager.  
* Familiarity with the command line or terminal.  
* Basic understanding of Python and REST APIs.

## **Part 1: Setup and The First Test Cycle**

### **Step 1: Setting Up Your Environment**

First, let's create a project directory and a virtual environment to keep our dependencies isolated.

1. Create a new directory for your project and navigate into it:  
   mkdir tdd-flask-todo  
   cd tdd-flask-todo

2. Create and activate a virtual environment:  
   * **macOS/Linux:**  
     ```bash
     python3 -m venv venv  
     source venv/bin/activate
     ```

   * **Windows:** 
    ```bash
     python -m venv venv  
     .venv\Scripts\activate
     ```

3. Install the necessary packages: Flask for our web application and pytest for testing.  
   ```bash
   pip install Flask pytest
   ```

### **Step 2: The First Test (The "RED" phase)**

In TDD, we always start by writing a failing test. This test defines what we want our code to do.

1. Create a new file named test\_app.py.  
2. Inside test\_app.py, write a test for the root endpoint (/).  


3. Run the test. It will fail with an ImportError because app.py doesn't exist. This is the **RED** phase.  
   pytest

### **Step 3: Make the Test Pass (The "GREEN" phase)**

Write the minimum code to make the test pass.

1. Create app.py.  
2. Add the following code:  
   \# app.py  
   from flask import Flask, jsonify

   app \= Flask(\_\_name\_\_)

   @app.route('/')  
   def index():  
       return "Welcome to the To-Do API\!"

   \# In-memory data store  
   todos \= \[  
       {"id": 1, "task": "Learn TDD", "done": False},  
       {"id": 2, "task": "Build a Flask API", "done": True},  
   \]

3. Run the tests again. It will pass. This is the **GREEN** phase.

### **Step 4: Refactor**

The code is simple, so no refactoring is needed yet.

## **Part 2: Adding Features with TDD**

Follow the Red-Green-Refactor cycle for each new feature. The process is detailed in the previous version of this document and involves adding endpoints for getting all todos, getting a single todo, and creating a todo, all while using the in-memory todos list. (Assume you have completed this part).

## **Part 3: Migrating to a Persistent Database with TDD**

Our API works, but the data is not persistent. We will now refactor the application to use an SQLite database. We'll use TDD to guide this significant change, ensuring our application continues to work as expected at every step.

### **Step 3.1: Install New Dependency**

First, add Flask-SQLAlchemy to your environment.

pip install Flask-SQLAlchemy

### **Step 3.2: Write a Failing Test for the Database (RED)**

Our goal is to make the *tests* use a database first. We will modify test\_app.py to set up and tear down a clean in-memory database for each test run. The application code (app.py) still uses the old in-memory list, so this change will break our tests and put us in the **RED** phase.

1. **Modify test\_app.py**. Replace its entire content with the code below. We are:  
   * Importing db and Todo (which don't exist in app.py yet).  
   * Changing the app fixture to configure a temporary in-memory database.  
   * Changing the client fixture to create the database tables, add sample data, and clean up afterward.

\# test\_app.py  
import pytest  
import json  
\# We are anticipating these imports from our future app.py  
from app import app as flask\_app, db, Todo

@pytest.fixture  
def app():  
    \# Configure the app for testing with an in-memory database  
    flask\_app.config\['SQLALCHEMY\_DATABASE\_URI'\] \= 'sqlite:///:memory:'  
    flask\_app.config\['TESTING'\] \= True  
    yield flask\_app

@pytest.fixture  
def client(app):  
    """A test client for the app. Manages DB setup and teardown."""  
    with app.app\_context():  
        db.create\_all() \# Create tables  
        \# Add initial data to the test database  
        todo1 \= Todo(task="Learn TDD", done=False)  
        todo2 \= Todo(task="Build a Flask API", done=True)  
        db.session.add(todo1)  
        db.session.add(todo2)  
        db.session.commit()

        yield app.test\_client() \# This is where the testing happens

        db.session.remove()  
        db.drop\_all() \# Drop all tables to ensure test isolation

def test\_index(client):  
    \# This test remains the same  
    response \= client.get('/')  
    assert response.status\_code \== 200  
    assert b"Welcome to the To-Do API\!" in response.data

def test\_get\_todos(client):  
    response \= client.get('/todos')  
    assert response.status\_code \== 200  
    assert len(response.json) \== 2 \# Expecting 2 from our test DB

\# ... keep the rest of your tests (get\_single, add\_todo, etc.)

2. **Run pytest**. The tests will fail with ImportError: cannot import name 'db' from 'app'. This is perfect\! Our test is telling us exactly what to do next: define db and Todo in our application.

### **Step 3.3: Make the Tests Pass (GREEN)**

Now, we modify app.py piece by piece to satisfy the new test conditions.

1. **Initialize the database in app.py**. Add the SQLAlchemy setup and the Todo model. At this point, your routes are still using the old todos list.  
   \# In app.py  
   from flask import Flask, jsonify, request  
   from flask\_sqlalchemy import SQLAlchemy  
   import os

   basedir \= os.path.abspath(os.path.dirname(\_\_file\_\_))  
   app \= Flask(\_\_name\_\_)  
   app.config\['SQLALCHEMY\_DATABASE\_URI'\] \= 'sqlite:///' \+ os.path.join(basedir, 'todos.db')  
   app.config\['SQLALCHEMY\_TRACK\_MODIFICATIONS'\] \= False

   db \= SQLAlchemy(app)

   class Todo(db.Model):  
       id \= db.Column(db.Integer, primary\_key=True)  
       task \= db.Column(db.String(200), nullable=False)  
       done \= db.Column(db.Boolean, default=False, nullable=False)

       def to\_dict(self):  
           return {'id': self.id, 'task': self.task, 'done': self.done}

   with app.app\_context():  
       db.create\_all()

   \# Your old routes using the 'todos' list are still here...  
   @app.route('/')  
   \# ...

   Run pytest again. The import error is gone, but now the tests for /todos fail because the routes are still returning the hardcoded list, not the data from the test database.  
2. **Update the API Endpoints.** Now, modify each endpoint to use the database session (db.session) instead of the todos list.  
   \# Replace the old routes in app.py with these database-aware versions  
   @app.route('/')  
   def index():  
       return "Welcome to the To-Do API\!"

   @app.route('/todos', methods=\['GET', 'POST'\])  
   def handle\_todos():  
       if request.method \== 'POST':  
           data \= request.get\_json()  
           if not data or 'task' not in data:  
               return jsonify({"error": "Missing task data"}), 400  
           new\_todo \= Todo(task=data\['task'\], done=data.get('done', False))  
           db.session.add(new\_todo)  
           db.session.commit()  
           return jsonify(new\_todo.to\_dict()), 201  
       else: \# GET  
           all\_todos \= Todo.query.all()  
           return jsonify(\[todo.to\_dict() for todo in all\_todos\])

   @app.route('/todos/\<int:todo\_id\>', methods=\['GET'\])  
   def get\_todo(todo\_id):  
       todo \= db.session.get(Todo, todo\_id)  
       if todo is None:  
           return jsonify({"error": "Todo not found"}), 404  
       return jsonify(todo.to\_dict())

3. **Run pytest one last time.** All tests should now pass. We are in the **GREEN** phase. We successfully migrated to a database-backed application, and our tests confirm that all functionality remains correct.

### **Step 3.4: Refactor**

Look at the new code in app.py. Is it clean and readable? In this case, the SQLAlchemy code is quite standard and doesn't require much refactoring. The TDD process for this migration is complete.

## **Further Challenges (Optional)**

Apply the TDD cycle to add database-backed features for:

1. **Update a To-Do Item (PUT /todos/\<id\>)**  
2. **Delete a To-Do Item (DELETE /todos/\<id\>)**