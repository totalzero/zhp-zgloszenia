# Zobaczyć Morze - System Zgłoszeń

System zgłoszeń na rejsy żeglarskie dla osób z dysfunkcją wzroku, prowadzony przez Fundację Zobaczyć Morze.

## Wymagania

- Python 3.12 lub nowszy
- pip (menedżer pakietów Python)

## Instalacja

### Instalacja tradycyjna (pip) - zalecana

1. **Utwórz wirtualne środowisko Python:**

   ```bash
   python -m venv venv
   ```

2. **Aktywuj wirtualne środowisko:**

   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Zainstaluj zależności:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Zainstaluj poethepoet (task runner):**

   ```bash
   pip install poethepoet
   ```

### Instalacja z UV (alternatywna)

Jeśli używasz [UV](https://github.com/astral-sh/uv):

```bash
uv sync
uv tool install poethepoet
```

## Pierwsze uruchomienie

Po instalacji wykonaj następujące kroki:

```bash
poe setup
```

Ta komenda wykona:
- Migracje bazy danych (`migrate`)
- Utworzenie konta administratora (`createsuperuser`)

Podczas tworzenia konta administratora:
- Podaj login, email i hasło
- Jeśli hasło jest za krótkie, potwierdź mimo to

## Kolejne uruchomienia

Aby uruchomić serwer deweloperski:

```bash
poe serve
```

Następnie otwórz przeglądarkę i wpisz adres:
- **Strona główna:** http://localhost:8000
- **Panel administracyjny:** http://localhost:8000/admin

## Komendy deweloperskie

| Komenda | Opis |
|---------|------|
| `poe serve` | Uruchom serwer deweloperski |
| `poe migrate` | Zastosuj migracje bazy danych |
| `poe createsuperuser` | Utwórz konto administratora |
| `poe setup` | Pierwsze uruchomienie (migrate + createsuperuser) |

**Uwaga:** Jeśli używasz UV, poprzedź komendy `uv run`, np. `uv run poe serve`.

## Struktura projektu

```
zobaczycmorze-zgloszenia/
├── rejs/                   # Główna aplikacja Django
│   ├── migrations/         # Migracje bazy danych
│   ├── static/css/         # Arkusze stylów
│   ├── templates/          # Szablony HTML
│   ├── models.py           # Modele danych
│   ├── views.py            # Widoki
│   ├── forms.py            # Formularze
│   ├── admin.py            # Konfiguracja panelu admina
│   └── signals.py          # Sygnały (np. wysyłanie emaili)
├── zm_zgloszenia/          # Ustawienia projektu Django
│   └── settings.py         # Konfiguracja
├── manage.py               # Skrypt zarządzania Django
├── pyproject.toml          # Konfiguracja projektu i zadań
├── requirements.txt        # Zależności (dla pip)
└── README.md               # Ten plik
```

## Grupy użytkowników

System posiada trzy predefiniowane grupy użytkowników:

| Grupa | Uprawnienia |
|-------|-------------|
| **Administratorzy** | Pełny dostęp do wszystkich funkcji |
| **Koordynatorzy Rejsów** | Zarządzanie rejsami, wachtami i ogłoszeniami |
| **Obsługa Zgłoszeń** | Zarządzanie zgłoszeniami i wpłatami |

Grupy są tworzone automatycznie podczas migracji. Przypisz użytkowników do grup w panelu administracyjnym: http://localhost:8000/admin/auth/group/

## Panel administracyjny

Po zalogowaniu do panelu admina (http://localhost:8000/admin) możesz:

- Dodawać i edytować rejsy
- Przeglądać i zarządzać zgłoszeniami
- Rejestrować wpłaty i zwroty
- Przypisywać uczestników do wacht
- Publikować ogłoszenia dla uczestników

Panel jest zaprojektowany tak, aby był prosty i intuicyjny. Jeśli masz problemy z obsługą, zgłoś to.
