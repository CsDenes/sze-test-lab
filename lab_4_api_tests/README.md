# **API Tesztelés**

## Kiindulás

Adott egy (előző labargyakorlaton fejlesztett) Flask alkalmazás az `app.py`.

## Feladat 1

## A projekt beállítás

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

## Bevezetés és Célok

A laborgyakorlat célja egy Python **Flask REST API** funkcionális tesztelésére szolgáló **Postman Környezet** és a teljes **CRUD** (Create, Read, Update, Delete) folyamatot lefedő **automatizált tesztek** (JavaScript kódok) létrehozása. A fő hangsúly a dinamikus adatok, mint az újonnan létrehozott ID-k, környezeti változókban történő kezelésén van.

## Előkészületek és Környezet Beállítása

1. Flask Alkalmazás Futtatása: Indítsa el a megadott Flask alkalmazást. 

```bash
flask run
```

Az elérési út ez lesz: `http://127.0.0.1:5000`.

2. Postman Környezet Létrehozása: Hozzon létre egy új Postman Environment-et a következő változókkal:  
   * **`baseURL`**: Értéke legyen `http://127.0.0.1:5000`. (Ezt használja a kérések URL-jében: `{{baseURL}}/todos`).  
   * **`newTodoId`**: Hagyja üresen; ezt a változót a **POST** kérés fogja beállítani.  
3. **Kérés Setup:** Hozzon létre egy új Postman Collectiont, és a következő lépésekben szereplő kéréseket ebben a Collectionben hozza létre.


## Tesztesetek Implementálása (Postman JavaScript)

A következő lépésekben a létrehozott kérések **`Tests`** fülére illessze be és módosítsa a megadott JavaScript kódokat.

### 1. GET /todos: Összes Teendő Lekérése

**Kérés:** `GET {{baseURL}}/todos`

- A státuszkód legyen `200 OK`.

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

- A válasz egy JSON tömb legyen, és hossza legalább 2.

```javascript
pm.test("Response is an array", function () {
    pm.expect(pm.response.json()).to.be.an('array');
});

pm.test("Array has at least 2 initial items", function () {
    pm.expect(pm.response.json().length).to.be.at.least(2);
});
```

### 2. POST /todos: Új Teendő Létrehozása (ID Mentése)

**Kérés:** `POST {{baseURL}}/todos`
**Body:** `raw` / `JSON` \-\> `{"task": "Postman teszteles beallitasa"}`

- A státuszkód legyen **`201 Created`**.

```javascript
pm.test("Status code is 201 (Created)", function () {
    pm.response.to.have.status(201);
});
```

- Környezeti Változó Beállítása: Mentse el a válaszban kapott `id` értékét a `newTodoId` környezeti változóba. Ez teszi lehetővé a láncolt tesztelést.

```javascript
const responseJson = pm.response.json();
pm.test("Set newTodoId for subsequent tests", function () {
    pm.environment.set("newTodoId", responseJson.id);
    console.log("New Todo ID saved: " + pm.collectionVariables.get("newTodoId"));
});
```

### 3. GET /todos/{{newTodoId}}: Egyedi Lekérése

**Kérés:** `GET {{baseURL}}/todos/{{newTodoId}}`

- A státuszkód legyen **`200 OK`**.

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

- A visszaadott teendő `id`-ja egyezzen meg a környezeti változóban tárolt értékkel.

```javascript
const responseJson = pm.response.json();
pm.test("Returned ID matches the saved ID", function () {
    // Ensure the ID of the fetched todo matches the one we created
    pm.expect(responseJson.id).to.eql(pm.environment.get("newTodoId"));
});
```

### 4. PUT /todos/{{newTodoId}}: Teendő Frissítése

**Kérés:** `PUT {{baseURL}}/todos/{{newTodoId}}`
**Body:** `raw` / `JSON` \-\> `{"done": true}`

- A státuszkód legyen `200 OK`.

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

- Ellenőrizze, hogy a válaszban a `done` mező értéke `true` lett.

```javascript
pm.test("Todo is marked as done: true", function () {
    pm.expect(pm.response.json().done).to.eql(true);
});
```

### 5. DELETE /todos/{{newTodoId}}: Teendő Törlése

**Kérés:** `DELETE {{baseURL}}/todos/{{newTodoId}}`

- A státuszkód legyen `204 No Content`.

```javascript
pm.test("Status code is 204 (No Content)", function () {
    pm.response.to.have.status(204);
});
```

- A válasz törzse üres legyen.

```javascript
pm.test("Response body is empty (No Content)", function () {
    pm.expect(pm.response.text()).to.be.empty;
});
```

### 6. Negatív Teszt: POST/GET/DELETE: Érvénytelen Adattal


## Feladat 2: Postman tesztek automatizálása a Newman CLI segítségével

A Postman tesztgyűjtemény és a hozzá tartozó környezeti beállítások exportálásával a tesztek helyben is futtathatók a Newman parancssori eszköz segítségével.

### Helyi futtatás Newman CLI-vel

Newman telepítése (ha még nem történt meg):

```bash
npm install -g newman
```


Test Collection futtatása  

```bash
newman run collection.json -e environment.json
```


### Postman tesztek futtatása GitHub workflow-ban

A Postman tesztek automatizált futtatásához egészítsd ki a .github/workflows mappában található ci.yaml fájlt. 
A cél, hogy az alkalmazás elindítása után a workflow automatikusan lefuttassa az exportált Postman kollekciót a Newman segítségével.

```bash
      # Step 5: Start Flask server
      - name: 🚀 Start Flask Server in Background
        run: |
          # Use '&' to run the server in the background
          # You may need to adjust the command based on your Flask file/setup (e.g., 'flask run' or 'python app.py')
          FLASK_APP=app.py flask run &
          # Give the server a moment to start up
          sleep 5 
      
      # Step 6: Install Newman
      - name: 📦 Install Newman (Postman CLI)
        run: npm install -g newman
      
      # Step 7: Run Postman tests using Newman
      - name: 🧪 Run Postman Tests with Newman
        run: |
          newman run collection.json \
            --environment environment.json
```

