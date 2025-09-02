# Feladat 1

A TDD-ben mindig egy hibát produkáló (failing) teszt megírásával kezdünk. Ez a teszt határozza meg, hogy mit várunk el a kódunktól

A teszt a `test_app.py` fileban található

Az Flask web alkalmazás a következővel paranccsal futtatható:

```bash
flask run
```

Majd az alkalmazás böngészőben itt megnyitható: `http://127.0.0.1:5000`

## Feladatok

1. Futtasd a teszteket `pytest` segítségével

```
pytest
```

2. Hozd működésbe a tesztet (a "ZÖLD" fázis), írd meg a lehető legkevesebb kódot, ami ahhoz szükséges, hogy a teszt sikeres legyen

3. Fejleszd tovább az alkalmazást hogy képes legyen új TODO elem hozzáadására

- Készítsd el először a tesztet a `test_app.py` fájlban
- Implementáld a POST hívást a `/todos` végponton is is az `app.py` fájlban
- Futtasd az alkalmazást és küldj POST hívást a `todos` végpontra  
  
  `curl -X POST -H "Content-Type: application/json" -d '{"task": "Finish the project"}' http://127.0.0.1:5000/todos`
