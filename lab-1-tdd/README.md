# Tesztvezérelt fejlesztés (TDD) Flask és Pytest segítségével

Ez az útmutató összefoglalja a tesztvezérelt fejlesztés (TDD) alapelveit, ahogy az a Flask alkalmazásoknál a Pytest keretrendszerrel alkalmazható.

## A TDD ciklus
A TDD egy olyan szoftverfejlesztési folyamat, amely egy nagyon rövid fejlesztési ciklus ismétlésén alapul:
- Piros: Írj egy olyan tesztet az új funkcióhoz, ami hibát ad.
- Zöld: Írd meg a teszt átmenetéhez szükséges minimális kódot.
- Refaktor: Tisztítsd meg a kódot, miközben gondoskodsz róla, hogy minden teszt továbbra is átmenjen.

Ez az iteratív folyamat biztosítja, hogy minden kódot teszt támogasson, ami robusztusabb és könnyebben karbantartható alkalmazásokhoz vezet.

## A projekt beállítás

Forkold ezt a GitHub repository-t, majd klónozhatod a helyi gépedre: [Github projekt](https://github.com/CsDenes/sze-test-lab/tree/main)

### Telepítés

Nyiss meg egy terminált és futtasd a következő parancsokat, amivel létrehozunk egy python virtuális környezetet és telepítjuk a szükséges csomagokat.

```bash
# Hozz létre és aktiválj egy virtuális környezetet
python -m venv venv
source venv/bin/activate

# Telepítsd a szükséges könyvtárakat
pip install Flask pytest

```

## Feladatok

[Feladat 1](feladat_1)