# Flask API Frontend Generálása és UI Tesztelés

## Célkitűzés

A laborfeladat célja, hogy megismerkedjünk a Google AI Studio használatával egy létező backend API-hoz (Flask) történő felhasználói felület (UI) generálásával. A feladat második fele a generált UI automatizált tesztelése egy Python alapú eszközzel (Selenium) a funkcionális helyesség ellenőrzésére.

## A Kiinduló Backend API

A feladathoz biztosítunk egy egyszerű Flask To-Do API-t. Ez egy memóriában tárolja a teendőket, és teljes CRUD (Create, Read, Update, Delete) funkcionalitást biztosít JSON-on keresztül.

A kód az `app.py` fájlban található.

### **Az API Endpontok:**

* `GET /todos`: Visszaadja az összes teendőt.  
* `POST /todos`: Létrehoz egy új teendőt. A JSON törzsnek tartalmaznia kell egy `task` kulcsot.  
* `GET /todos/<id>`: Visszaad egy teendőt az ID-ja alapján.  
* `PUT /todos/<id>`: Frissít egy meglévő teendőt (pl. `task` vagy `done` állapot).  
* `DELETE /todos/<id>`: Töröl egy teendőt az ID-ja alapján.

## Feladatok

### Backend Elindítása

Mentsd el a mellékelt `app.py` kódot.

Telepítsd a szükséges csomagot:

```bash 
pip install flask flask-cors 
```

```bash
flask run
```

Az API mostantól a `http://127.0.0.1:5000` címen érhető el. Ellenőrizd egy böngészőben vagy `curl` segítségével (`curl http://127.0.0.1:5000/todos`).

### A Frontend (UI) Generálása az AI Studio-ban

1. Nyisd meg a Google AI Studio-t.  
2. Hozz létre egy új "prompt"-ot. A cél egy olyan egyfájlos HTML, CSS és JavaScript alkalmazás generálása, amely képes kommunikálni a futó Flask API-val.

**Ajánlott Prompt (Induló pontként):**

```
Create a one file html site using only CSS and Javascript for the following Flask Python backend:   
\<insert your code\>  
Use only one html file and the backend is running on http://127.0.0.1:5000.
```

**Integráció és Tesztelés:**

Töltsd le a generált htlm kódot és futtasd a következő parancssal:

```bash
python -m http.server 9000
```

### UI Automatikus Tesztelése

Miután a UI manuálisan működik, írunk egy automatizált tesztet, hogy ellenőrizzük a fő funkciókat. Ehhez a Selenium csomagot használjuk.

**Telepítés:**

```bash 
pip install selenium webdriver-manager
```

1. **A Teszt Kód (`test_ui.py`):**  
   * A mellékelt `test_ui.py` egy sablon, ami `unittest` és `selenium` segítségével teszteli az alkalmazást.  
   * A szkript automatikusan letölti és kezeli a megfelelő `chromedriver`\-t a `webdriver-manager` segítségével.  
2. **A Teszt Adaptálása:**  
   * Az AI által generált HTML kód valószínűleg más ID-kat vagy osztályneveket használ, mint amiket a teszt sablon feltételez (pl. `new-task-input`, `add-task-button`, `todo-list`).  
   Nyisd meg az `index.html`\-t és a böngésző "Developer Tools" (F12) segítségével azonosítsd a megfelelő HTML elemek szelektorait (ID, class, XPath, stb.).  
   Frissítsd a `test_ui.py` fájlban a szelektorokat (pl. `find_element(By.ID, "...")`), hogy azok megfeleljenek a generált kódodnak.  
3. **A Teszt Futtatása:**  
   * Győződj meg róla, hogy a Flask szerver (`app.py`) fut (`http://127.0.0.1:5000`).  
   * Futtasd a tesztet a terminálból (győződj meg róla, hogy az `index.html` elérési útja helyes a `self.driver.get(...)` hívásban):

```bash
python -m unittest test_ui.py
```
