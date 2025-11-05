# Python Flask API Terheléses Tesztelése

**A feladat célja:** A labor során megismerkedünk a webes API-k (Application Programming Interface) terheléses tesztelésének alapjaival a `locust` keretrendszer segítségével. A cél egy egyszerű Python Flask alkalmazás teljesítményének mérése, a szűk keresztmetszetek (bottlenecks) azonosítása és a terhelés alatti viselkedés elemzése.

## A Tesztelendő Alkalmazás (`app.py`)

A feladathoz adott egy előkészített, memóriában tárolt "Todo" listát kezelő Flask API.

**Főbb végpontok:**

* `GET /`: Egyszerű üdvözlőoldal.  
* `GET /todos`: Visszaadja az összes todo elemet.  
* `POST /todos`: Létrehoz egy új todo elemet a küldött JSON body alapján.  
* `GET /todos/<id>`: Visszaad egy specifikus todo elemet az azonosítója alapján.  
* `PUT /todos/<id>`: Módosít egy létező todo elemet.  
* `DELETE /todos/<id>`: Töröl egy létező todo elemet.

Az alkalmazás (az `app.py` fájl) a Flask beépített szerverével is futtatható, de a valósághű teszteléshez egy produkciós WSGI szervert, például `gunicorn`\-t fogunk használni.

## A Teszt-szkript (`locustfile.py`)

A terhelést a `locust` eszközzel szimuláljuk. A `locustfile.py` definiálja, hogyan viselkedjenek a "felhasználók".

**Szimulált viselkedés:**

* `get_all_todos` (súly: 3): A felhasználók leggyakrabban az összes todo listáját kérik le.  
* `get_single_todo` (súly: 2): Gyakran néznek meg egy-egy elemet (a tesztben az 1-es vagy 2-es ID-jűt).  
* `create_todo` (súly: 1): Ritkábban új elemet hoznak létre.  
* `update_todo` (súly: 1): Ritkábban egy meglévő elemet módosítanak.  
* `get_root` (súly: 1): Ritkán a kezdőoldalt is meglátogatják.

A `wait_time = between(1, 2.5)` beállítás biztosítja, hogy a felhasználók 1 és 2.5 másodperc közötti véletlenszerű időt várjanak a kéréseik között, így szimulálva a valós böngészést.

## Feladatok

### A projekt beállítás

- Nyisd meg a Visual Studio Code alkalmazást
- Nyiss egy új terminált és válaszd ki a git bash opciót
- Forkold ezt a GitHub repository-t, majd klónozhatod a helyi gépedre: [Github projekt](https://github.com/CsDenes/sze-test-lab/tree/main)

```bash
git clone https://github.com/<felhasznalo>/sze-test-lab/tree/main
```

Nyiss meg egy terminált és futtasd a következő parancsokat, amivel létrehozunk egy python virtuális környezetet és telepítjuk a szükséges csomagokat.

```bash
# feladat kiválasztás
cd lab_5_load_tests
# Hozz létre és aktiválj egy virtuális környezetet
python -m venv venv
source venv/Scripts/activate

# Telepítsd a szükséges könyvtárakat
pip install flask locust gunicorn
``` 

### Az API Alkalmazás Futtatása

A teszteléshez egy produkciós szerverre van szükségünk. Nyiss egy terminált, és futtasd az alkalmazást a `gunicorn` segítségével.

Futtasd az `app.py`-t a gunicorn szerverrel, 1 workerrel, az 5000-es porton

```bash 
gunicorn --workers 1 --bind localhost:5000 app:app
```

**Fontos:** Ezt a terminált hagyd futni a háttérben. Az API mostantól elérhető a `http://localhost:5000` címen.

### A Terheléses Teszt Indítása

Nyiss egy **másik** terminált (az elsőt hagyd futni), és indítsd el a `locust` tesztelőt.

```bash
locust -f locustfile.py
```

Ha sikeres, a terminálban látnod kell egy üzenetet, ami jelzi, hogy a Locust webes felülete elindult: `[... INFO] Starting web interface at http://0.0.0.0:8089`

### A Teszt Konfigurálása és Futtatása

1. Nyisd meg a böngésződben a terminálban jelzett címet: **`http://localhost:8089`**.  
2. Egy beállító felület fogad. Töltsd ki az alábbi mezőket:  
   * **Number of users:**  Szimulált felhasználók száma  
   * **Ramp up:** Hány felhasználó induljon el másodpercenként  
   * **Host:** `http://localhost:5000` (A tesztelendő API címe, amit a `gunicorn` futtat)  
3. Kattints a **"Start"** gombra.

## Elemzés és Kérdések

A teszt elindulása után figyeld a Locust felület "Statistics", "Charts" és "Failures" füleit. Futtasd a tesztet legalább 1-2 percig.

**Válaszold meg az alábbi kérdéseket:**

1. **Alap terhelés (100 felhasználó):**  
   * Mennyi a teljes **RPS** (Requests Per Second, kérések száma másodpercenként) átlagosan?  
   * Mennyi a **Median (50%)** és a **95th percentile** válaszidő (Response Time) a `GET /todos` végpont esetében?  
   * Látsz-e "Failures" (hibás kérések) fülön bármilyen hibát?  
   * A `gunicorn` termináljában látod-e a beérkező kéréseket?  
2. **Magas terhelés (Stressz teszt):**  
   * Állítsd le a tesztet ("Stop" gomb), majd indíts egy újat ("New test") a következő beállításokkal: **Number of users: `1000`**, **Ramp up: `100`**.  
   * Hogyan változott az RPS? Növekedett arányosan (tízszeresére)?  
   * Mi történt a válaszidőkkel (Response Times)? Különösen a 95th percentile értékkel?  
   * Megjelentek-e hibák ("Failures")? Ha igen, milyen típusúak és melyik végponton?  
3. **Elemzés:**  
   * A `locustfile.py` alapján melyik végpont kapja a legtöbb kérést? Hogyan tükröződik ez a "Statistics" táblázat "Requests" oszlopában?  
   * Mit gondolsz, mi okozhatja a válaszidő növekedését és a hibák megjelenését magas terhelés alatt?  
   * Milyen az alkalmazás memória és cpu használata tesztelés során? Hol látod ezt?

## **Bónusz Feladat**

Módosítsd a `locustfile.py`\-t úgy, hogy a `DELETE` végpontot is tesztelje. Hogyan oldod meg, hogy a `DELETE` feladat ne fusson hibára azzal, hogy megpróbál nem létező elemet törölni? (Tipp: A `create_todo` feladatban elmentheted a létrehozott elem ID-ját egy listába, amiből a `DELETE` feladat véletlenszerűen választhat.)