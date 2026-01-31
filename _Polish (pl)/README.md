# Zestaw Narzędzi CLI (Python)

Zbiór skryptów i modułów w języku Python tworzących środowisko CLI (Command Line Interface) do zarządzania plikami, edycji tekstu, gier i narzędzi systemowych.

**Autor:** Sebastian Januchowski  
**Kontakt:** polsoft.its@fastservice.com  
**GitHub:** https://github.com/seb07uk  

## Struktura Projektu

### Główne Aplikacje
| Plik | Opis |
|------|------|
| `CMD File Manager Cli v1.5.0 (pl).py` | Menedżer plików CMD Cli: Pełny pakiet z historią i szybkimi linkami. |
| `Simple Notepad v1.5 (pl).py` | Prosty Notatnik PRO z funkcją AutoSave i szybką nawigacją. |
| `Paint Cli v1.0.py` | Konsolowy program graficzny (Paint) z obsługą kolorów i zapisem projektów. |

### Moduły (katalog `moduly`)
| Plik | Kategoria | Opis |
|------|-----------|------|
| `core.py` | core | Przeglądarka modułów rdzenia - wyświetla kluczowe wtyczki systemowe. |
| `print (modul).py` | io | Narzędzie do wyświetlania plików z kolorowaniem składni (cat/type). |
| `Generator Listy (modul).py` | file list | Generator listy plików w terminalu. |
| `Kalkulator Pro v1.8 (modul) pl.py` | math | Profesjonalny kalkulator naukowy z logowaniem historii. |
| `Games Menu (modul).py` | rozrywka | Centrum Gier - dynamiczny launcher dla gier konsolowych. |

### Gry (katalog `gry`)
| Plik | Kategoria | Opis |
|------|-----------|------|
| `Snake CLI.py` | games | Gra Snake w stylu retro ze skórkami, poziomami trudności i rankingiem. |

## Wymagania Systemowe
*   **Python 3.x**
*   **System:** Windows (zalecane ze względu na użycie biblioteki `msvcrt` do obsługi klawiatury i komend systemowych) lub Linux (częściowa kompatybilność).
*   **Zależności:** Standardowa biblioteka Python (brak zewnętrznych wymagań pip).

## Konfiguracja
Większość aplikacji automatycznie tworzy strukturę katalogów dla danych i konfiguracji w folderze użytkownika:
`%USERPROFILE%\.polsoft\psCLI\`

## Uruchamianie
Skrypty można uruchamiać bezpośrednio z konsoli, np.:
```bash
python "CMD File Manager Cli v1.5.0 (pl).py"
```

---
*Dokument wygenerowany automatycznie na podstawie analizy plików źródłowych.*