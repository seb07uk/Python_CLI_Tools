import os
import sys
import re
import subprocess
from cli import command, Color

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "rozrywka"
__group__ = "menu"
__desc__ = "Centrum Gier - dynamiczny launcher dla gier konsolowych"

HEADER = r"""
          ,o888888o.            .8.                    ,8.        ,8.            8 8888888888      d888888o.
         8888     `88.         .888.                  ,888.      ,888.           8 8888            .`8888:' `88.
      ,8 8888       `8.       :88888.                .`8888.    .`8888.          8 8888            8.`8888.   Y8
      88 8888                . `88888.              ,8.`8888. ,8.`8888.          8 8888            `8.`8888.
      88 8888               .8. `88888.            ,8'8.`8888,8^8.`8888.         8 888888888888    `8.`8888.
      88 8888              .8`8. `88888.          ,8' `8.`8888' `8.`8888.        8 8888             `8.`8888.
      88 8888   8888888   .8' `8. `88888.        ,8'   `8.`88'   `8.`8888.       8 8888              `8.`8888.
      `8 8888       .8'  .8'   `8. `88888.      ,8'     `8.`'     `8.`8888.      8 8888           8b   `8.`8888.
         8888     ,88'  .888888888. `88888.    ,8'         `8          `8.`8888.  8 8888           `8b.  ;8.`8888
          `8888888P'   .8'         `8. `88888. ,8'            `          `8.`8888. 8 888888888888   `Y8888P ,88P
"""

GAMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "games"))

def get_metadata(file_path):
    """Skanuje plik gry w poszukiwaniu __desc__ bez jego importowania."""
    meta = {"desc": "Brak dostępnego opisu"}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            desc_match = re.search(r'__desc__\s*=\s*["\'](.*?)["\']', content)
            if desc_match:
                meta["desc"] = desc_match.group(1)
    except Exception:
        pass
    return meta

def show_help():
    """Wyświetla instrukcje i informacje o autorze dla Modułu Gier."""
    print(f"\n{Color.BOLD}--- CENTRUM GIER - POMOC ---{Color.RESET}")
    print(f"Ten moduł służy jako dynamiczny launcher dla samodzielnych gier Python.")
    print(f"1. {Color.GREEN}Listowanie:{Color.RESET} Skanuje katalog '../games/' w poszukiwaniu plików .py.")
    print(f"2. {Color.GREEN}Metadane:{Color.RESET} Automatycznie odczytuje zmienną '__desc__' z plików.")
    print(f"3. {Color.GREEN}Uruchamianie:{Color.RESET} Gry są otwierane w osobnym oknie terminala.")
    
    print(f"\n{Color.YELLOW}Komendy:{Color.RESET}")
    print(f" - [ID]: Wpisz numer, aby uruchomić grę.")
    print(f" - [Nazwa]: Wpisz nazwę pliku (bez .py), aby uruchomić.")
    print(f" - 'help' lub '?': Wyświetl te informacje.")
    print(f" - 'q', 'exit', 'quit': Powrót do głównego menu CLI.")
    
    # Sekcja autora na dole
    print(f"\n{Color.GRAY}{'-' * 40}")
    print(f"autor:   Sebastian Januchowski")
    print(f"email:   polsoft.its@fastservice.com")
    print(f"github:  https://github.com/seb07uk")
    print(f"         2026© polsoft.ITS London{Color.RESET}\n")

@command(name="games", aliases=["play", "g", "gry"])
def games_dispatcher(*args):
    """Launcher gier dla TERMINAL CLI."""
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)

    print(f"{Color.CYAN}{HEADER}{Color.RESET}")
    
    files = [f for f in os.listdir(GAMES_DIR) if f.endswith(".py") and f != "__init__.py"]
    
    if not files:
        print(f"{Color.YELLOW}[!] Folder /games jest pusty.{Color.RESET}")
        return

    print(f"{Color.BOLD}{'ID':<3} | {'GRA':<20} | {'OPIS'}{Color.RESET}")
    print(f"{Color.GRAY}{'-' * 80}{Color.RESET}")

    games_map = {}
    for idx, filename in enumerate(sorted(files), 1):
        name = filename[:-3]
        file_full_path = os.path.join(GAMES_DIR, filename)
        meta = get_metadata(file_full_path)
        
        games_map[str(idx)] = (name, file_full_path)
        games_map[name.lower()] = (name, file_full_path)
        
        print(f"{Color.GREEN}{idx:<3}{Color.RESET} | "
              f"{Color.WHITE}{name:<20}{Color.RESET} | "
              f"{meta['desc']}")

    while True:
        print(f"\n{Color.GRAY}Wpisz ID/Nazwę, 'help' dla pomocy, lub 'q' aby wyjść.{Color.RESET}")
        try:
            choice = input(f"{Color.CYAN}psGAMES > {Color.RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if choice in ['q', 'quit', 'exit']:
            break
        elif choice in ['help', '?']:
            show_help()
            continue
        elif choice in games_map:
            game_name, path = games_map[choice]
            print(f"{Color.YELLOW}[*] Uruchamianie {game_name} w nowym oknie...{Color.RESET}")
            try:
                subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            except Exception as e:
                print(f"{Color.RED}[BŁĄD] Nie można uruchomić gry: {e}{Color.RESET}")
        else:
            print(f"{Color.RED}[!] Nieznana komenda lub gra: {choice}{Color.RESET}")

if __name__ == "__main__":
    games_dispatcher()