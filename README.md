# Rozproszony system REST API - Serwis Produktów i Serwis Magazynowy

Projekt demonstruje komunikację między-serwisową w architekturze REST. Składa się z dwóch niezależnych mikroserwisów zaimplementowanych w języku Python z użyciem frameworka FastAPI.

## Architektura
1. **Product Service (Serwis Produktów)** - port `8001`. Zarządza bazą produktów.
2. **Stock Service (Serwis Magazynowy)** - port `8002`. Zarządza stanami magazynowymi, ale przed zwróceniem wyniku weryfikuje istnienie produktu w Serwisie Produktów.

## Wymagania
- Python w wersji 3.8 lub nowszej.

## Instrukcja instalacji środowiska

Aby uruchomić projekt, należy zainstalować wymagane biblioteki (m.in. `fastapi`, `uvicorn`, `httpx`). Zalecane jest użycie wirtualnego środowiska (virtual environment), aby nie zaśmiecać globalnych pakietów Pythona w systemie.

1. **Sklonuj lub pobierz repozytorium:**
   Pobierz pliki projektu na swój dysk i przejdź do folderu z projektem w terminalu (wierszu poleceń).

2. **Utwórz wirtualne środowisko:**
   Wpisz w terminalu poniższą komendę:
   ```bash
   python -m venv venv
   ```

3. **Aktywuj wirtualne środowisko:**
   - **Windows (Command Prompt / PowerShell):**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```
   *(Po poprawnej aktywacji, w terminalu po lewej stronie powinna pojawić się nazwa środowiska w nawiasie, np. `(venv)`).*

4. **Zainstaluj wymagane pakiety z pliku `requirements.txt`:**
   Mając aktywne środowisko, uruchom komendę:
   ```bash
   pip install -r requirements.txt
   ```

## Uruchomienie serwisów

Aplikacja składa się z dwóch niezależnych serwerów. Należy je uruchomić w dwóch osobnych oknach terminala (pamiętaj, aby w obu mieć aktywowane wirtualne środowisko `venv`!).

**Terminal 1 (Serwis Produktów):**
```bash
python product_service.py
```
*Serwis uruchomi się na porcie 8001.*

**Terminal 2 (Serwis Magazynowy):**
```bash
python stock_service.py
```
*Serwis uruchomi się na porcie 8002.*

## Ręczne testowanie API (Użytkowanie)

Ponieważ oba serwisy korzystają z metody HTTP `GET`, można je przetestować z poziomu zwykłej przeglądarki internetowej lub z poziomu terminala za pomocą narzędzia `curl`. Odpytujemy **Serwis Magazynowy** (port 8002), a on "pod spodem" odpyta **Serwis Produktów** (port 8001).

### Scenariusz 1: Sukces (Zapytanie o istniejący produkt)
W bazie istnieją produkty o ID `123` oraz `124`.

- **Przez przeglądarkę:** Otwórz link: http://127.0.0.1:8002/stock/123
- **Przez cURL (Terminal 3):** 
  ```bash
  curl [http://127.0.0.1:8002/stock/123](http://127.0.0.1:8002/stock/123)
  ```
**Oczekiwany wynik:** Zwrócony zostanie kod `200 OK` i JSON: `{"productId": 123, "quantity": 15}`. W logach serwerów będzie widać poprawną komunikację.

### Scenariusz 2: Błąd (Zapytanie o nieistniejący produkt)
Pytamy o produkt, którego nie ma w bazie (np. ID `999`).

- **Przez przeglądarkę:** Otwórz link: http://127.0.0.1:8002/stock/999
- **Przez cURL (Terminal 3):**
  ```bash
  curl [http://127.0.0.1:8002/stock/999](http://127.0.0.1:8002/stock/999)
  ```
**Oczekiwany wynik:** Zwrócony zostanie kod `404 Not Found` i JSON: `{"detail": "Product not found"}`. Serwis Magazynowy odrzuci zapytanie, ponieważ Serwis Produktów zgłosił brak takiego ID.
