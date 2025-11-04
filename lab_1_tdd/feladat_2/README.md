# Feladat 2

A TDD-ben mindig egy hibát produkáló (failing) teszt megírásával kezdünk. Ez a teszt határozza meg, hogy mit várunk el a kódunktól. Jelen feladat célja a Feladat 1 során létrehozott alkalmazás továbbfejlesztése: az eddigi memóriában történő adattárolás helyett most egy helyi SQL adatbázis segítségével kell megvalósítani az adatok tárolását.

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
