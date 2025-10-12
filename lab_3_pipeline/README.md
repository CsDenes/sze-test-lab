# Kód javítás és pipeline fejlesztés

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

## Kiindulási állapot

Adott egy egyszerű "To-Do" lista API, amely a `app.py` fájlban található. Az alkalmazáshoz tartoznak pytest és pytest-bdd tesztek is, amelyek lefedik a helyes működést. Az `app.py` fájl azonban 10 szándékos hibát tartalmaz, amelyek megakadályozzák a tesztek sikeres lefutását. A hibák nem elírások, hanem logikai, típuskezelési vagy API-szabványokkal kapcsolatos problémák.

## Feladat 1 - Hibajavítás

1. Futtasd a teszteket a pytest -v paranccsal a terminálban.

2. Elemezd a hibaüzeneteket

3. A tesztek visszajelzései alapján keresd meg a hibákat (10 db) a `app.py` fájlban, és javítsd ki őket.

## Feladat 2 - GitHub Actions CI Pipeline Létrehozása

Miután az alkalmazás helyesen működik és minden teszt sikeres, automatizáljuk a tesztelési folyamatot. Hoz létre egy GitHub Actions pipeline-t, amely minden push és pull_request eseménykor a main ágra automatikusan lefuttatja az összes tesztet.

1. Definiáld a függőségeket

Hozd létre a projekt gyökérkönyvtárában a `requirements.txt` fájlt a következő tartalommal. Ez a fájl mondja meg a GitHub Actions-nek, hogy milyen Python csomagokat kell telepítenie.

```bash
Flask
pytest
pytest-bdd
```

2. A workflow fájl létrehozása

A projekt gyökérkönyvtárában hozd létre a .github/workflows/ mappaszerkezetet. Ezen belül hozz létre egy ci.yml nevű fájlt.

3. A pipeline kódjának megírása

`.github/workflows/ci.yml`

- Add hozzá a triggert: `on`

- Hozd létre a `job`-ot

- 1. lépés hozzáadása ami letölti a repository kódját

- 2. lépés hozzáadása ami beállítja a python-t (`actions/setup-python@v4`)

- 3. lépés a függőségek telepítése (`pip install -r requirements.txt`)

- 4. lépés a tesztek futtatása

4. Státusz-jelvény (Status Badge) hozzáadása

Hogy a projekt főoldalán is látható legyen a tesztek aktuális állapota, adj hozzá egy státusz-jelvényt.

- Nyisd meg a repository-t a böngészőben, és kattints az Actions fülre.

- Válaszd ki a bal oldali listából az elkészített workflow-t.

- Kattints a "..." menüre a jobb felső sarokban, majd a Create status badge opcióra.

- Másold ki a felugró ablakból a Markdown kódot.

- Illeszd be a kimásolt kódot a README.md fájlod legelejére.
