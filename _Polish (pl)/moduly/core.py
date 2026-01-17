import os
import json
from cli import command, Color

# --- METADATA ---
__author__ = "Sebastian Januchowski"
__category__ = "core"
__group__ = "menu"
__desc__ = "Core Module Viewer - displays essential system plugins"

@command(name="core", aliases=["sys", "base"])
def core_viewer(*args):
    """Główna funkcja wyświetlająca pliki grupy core."""
    
    # Ścieżka do ustawień zgodnie z Twoją konfiguracją
    settings_file = os.path.expandvars(r"%userprofile%\.polsoft\psCli\settings\terminal.json")
    # Pobieramy ścieżkę do folderu plugins względem pliku core.py
    plugins_dir = os.path.dirname(__file__)

    if not os.path.exists(plugins_dir):
        print(f"{Color.RED}[BŁĄD] Katalog '{plugins_dir}' nie istnieje.{Color.RESET}")
        return

    print(f"{Color.CYAN}{Color.BOLD}--- LISTA PLIKÓW CORE ---{Color.RESET}")

    # Filtrujemy pliki .py, które zawierają frazę 'core' w nazwie
    files = [f for f in os.listdir(plugins_dir) if f.endswith('.py') and "core" in f.lower()]
    
    # Dodanie cls.py jako kluczowego elementu core, jeśli istnieje
    if os.path.exists(os.path.join(plugins_dir, "cls.py")):
        if "cls.py" not in files:
            files.append("cls.py")

    # Sortowanie i wyświetlanie zgodnie z Twoim schematem align: plik # opis
    for file in sorted(files):
        if file == "core.py":
            print(f"{Color.GREEN}{file:<20}{Color.RESET} {Color.GRAY}# Main core viewer module{Color.RESET}")
        elif file == "cls.py":
            # Align zgodny z Twoją prośbą: type plugins/cls.py # Displaying source code
            print(f"{Color.GREEN}type plugins/{file:<12}{Color.RESET} {Color.GRAY}# Displaying source code{Color.RESET}")
        else:
            print(f"{Color.GREEN}{file:<20}{Color.RESET} {Color.GRAY}# Core system plugin{Color.RESET}")

    print(f"{Color.CYAN}{'-' * 40}{Color.RESET}")

if __name__ == "__main__":
    core_viewer()