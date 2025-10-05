# Viselkedésvezérelt fejlesztés (BDD) Flask és Pytest-bdd segítségével

Egy új funkciót fogunk hozzáadni az alkalmazáshoz: egyetlen teendő (to-do) lekérdezését az azonosítója (ID) alapján.

Adott egy (előző labargyakorlaton fejlesztett) Flask alkalmazás az `app.py`. Ez jelenleg képes TODO elemeket hozzáadni egy listához illetve lekéréskor visszaadni ezt a listát.

## Feladat 1

Adjunk az alkalmazáshoz egy új funkciót ami képes visszaadni egyetlen teendőt (to-do) az azonosítója (ID) alapján. Ezt a BDD módszer használatával tegyük meg.

A BDD-ciklus, amit követni fogunk:

1. Viselkedés Leírása: Megírunk egy ember által is olvasható "feature" fájlt, ami leírja, hogyan kellene az új funkciónak működnie.

2. Lépésdefiníciók Megírása: Megírjuk a Python tesztkódot, ami a feature fájlban leírt lépésekhez kapcsolódik.

3. Futtatás és Hiba: Lefuttatjuk a teszteket, amelyek meg fognak hibásodni, mivel az alkalmazás kódja még nem létezik.

4. Alkalmazáskód Megírása: Implementáljuk a funkcionalitást a Flask alkalmazásban, hogy a tesztek sikeresek legyenek.

5. Futtatás és Siker: Újra lefuttatjuk a teszteket, hogy megbizonyosodjunk róla, a funkció a leírtak szerint működik.


### A projekt beállítás

- Nyisd meg a Visual Studio Code alkalmazást
- Nyiss egy új terminált és válaszd ki a git bash opciót
- Forkold ezt a GitHub repository-t, majd klónozhatod a helyi gépedre: [Github projekt](https://github.com/CsDenes/sze-test-lab/tree/main)

```bash
git clone https://github.com/<felhasznalo>/sze-test-lab/tree/main
```

Nyiss meg egy terminált és futtasd a következő parancsokat, amivel létrehozunk egy python virtuális környezetet és telepítjuk a szükséges csomagokat.

```bash
# Hozz létre és aktiválj egy virtuális környezetet
python -m venv venv
source venv/Scripts/activate

# Telepítsd a szükséges könyvtárakat
pip install Flask pytest pytest-bdd
```

A projektünket az alábbi struktúra szerint rendezzük be:

```bash
.
├── app.py
├── test_single_todo.py
├── features
   └── single_todo.feature
```

### 1. lépés: A Viselkedés Leírása (A Feature Fájl)

Létrehozunk egy Gherkin szintaxist használó "feature" fájlt, amely két forgatókönyvet (scenario) ír le: egy teendő sikeres megtalálását és egy nem létező teendő keresésének sikertelenségét.

Hozd létre a `features` mappát, és benne a `single_todo.feature` fájlt.

A fájlban definiáljuk magát a feature-t pl.:

```python
Feature: Retrieve a single To-Do item
  As a user of the API,
  I want to be able to retrieve a specific to-do item by its ID,
  so that I can view its details.
```

Majd adjunk hozzá Scenario-kat:

```python
  Scenario: A to-do item exists
    Given the API has a to-do with id 2 and task "Build a Flask API"
    When the user requests the to-do with id 2
    Then the response status code should be 200
    And the response should contain the details of the to-do with id 2

  Scenario: A to-do item does not exist
    Given the API has a list of to-dos
    When the user requests the to-do with id 99
    Then the response status code should be 404
    And the response should contain a "not found" error message
```

### 2. Lépés: A Lépésdefiníciók Megírása (A Tesztfájl)

Most implementáljuk a Python kódot, amelyet a pytest-bdd futtatni fog a .feature fájlunk minden egyes lépéséhez.

Add hozzá a különböző lépéseket a `test_single_todo.py` fájlhoz

- Elsőként adjuk hozzá a `given` lépéseket:

```python
# Given Steps
@given('the API has a to-do with id 2 and task "Build a Flask API"')
def setup_existing_todo():
    """Set up the initial state with a known to-do item."""
    # Ensure our 'todos' list is in a known state for this test
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        EXISTING_TODO,
    ]

@given('the API has a list of to-dos')
def setup_any_todos():
    """Set up the initial state with a generic list."""
    global todos
    todos[:] = [
        {"id": 1, "task": "Learn TDD", "done": False},
        {"id": 2, "task": "Build a Flask API", "done": True},
        {"id": 3, "task": "Example TODO", "done": False},
    ]
```

- Majd adjuk hozzá a when lépést is:

```python
# When Steps
@when(parsers.parse('the user requests the to-do with id {todo_id}'))
def get_single_todo(client, response, todo_id):
    """Make a GET request to the /todos/<id> endpoint."""
    res = client.get(f'/todos/{todo_id}')
    response['data'] = res.get_json()
    response['status_code'] = res.status_code
```

- Majd végül implementáljuk a `when` lépéseket is:

```python
# Then Steps
@then(parsers.parse('the response status code should be {status_code:d}'))
def check_status_code(response, status_code):
    """Check if the response status code is the expected one."""
    assert response['status_code'] == status_code

@then('the response should contain the details of the to-do with id 2')
def check_response_for_existing_todo(response):
    """Check the content of the response for a successful request."""
    assert response['data'] == EXISTING_TODO

@then('the response should contain a "not found" error message')
def check_response_for_not_found(response):
    """Check the content of the response for a 404 error."""
    assert 'error' in response['data']
    assert 'not found' in response['data']['error'].lower()
```

### 3. Lépés: Futtatás és Sikertelen Teszt

Ha most lefuttatod a teszteket, azok sikertelenek lesznek, mivel még nem implementáltuk a `/todos/<id>` útvonalat a Flask alkalmazásunkban.

```bash
pytest
```

### 4. Lépés: Az Alkalmazáskód Megírása

Most módosítsuk az `app.py` fájlt, hogy hozzáadjuk az új végpontot és sikeressé tegyük a tesztjeinket. Hozzáadunk egy új függvényt, ami egyetlen teendőre vonatkozó kéréseket kezel.

```python
@app.route('/todos/<int:todo_id>', methods=['GET'])
def handle_single_todo(todo_id):
    """
    Handles GET requests for a single to-do item by its ID.
    """
    # Find the todo with the matching ID
    todo = next((item for item in todos if item["id"] == todo_id), None)
    
    if todo:
        # If found, return the todo item with a 200 OK status
        return jsonify(todo), 200
    else:
        # If not found, return an error message with a 404 Not Found status
        return jsonify({"error": f"Todo with id {todo_id} not found"}), 404


def _get_next_id():
    """A helper function to get the next ID for a new todo."""
    # If the list is empty, start with ID 1. Otherwise, find the max ID and add 1.
    if not todos:
        return 1
    return max(todo['id'] for todo in todos) + 1
```

Mit adtunk hozzá:

- Egy új `/todos/<int:todo_id>` útvonalat, ami csak GET kéréseket fogad. Az `<int:todo_id>` rész jelzi a Flask-nek, hogy egy egész számot vár az URL-ben.

- A handle_single_todo(todo_id) függvényt, ami a todos listában megkeresi a megfelelő id-jú elemet.

- Ha az elem megtalálható, JSON formátumban, 200 OK státusszal tér vissza.

- Ha az elem nem található, egy hibaüzenetet ad vissza JSON formátumban, 404 Not Found státusszal. Ez mindkét forgatókönyvünket kielégíti.


## Feladat 2

Adjunk az alkalmazáshoz egy új funkciót ami képes törülni egyetlen teendőt (to-do) az azonosítója (ID) alapján. Ezt is hasonlóan az előző feladathoz a BDD módszer használatával tegyük meg.
