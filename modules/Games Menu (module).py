import os
import sys
import re
import subprocess
from cli import command, Color

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "entertainme."
__group__ = "menu"
__desc__ = "Game Center - dynamic launcher for external console games"

HEADER = r"""
          ,o888888o.           .8.                    ,8.       ,8.            8 8888888888      d888888o.
         8888     `88.        .888.                  ,888.     ,888.           8 8888           .`8888:' `88.
      ,8 8888       `8.      :88888.                .`8888.   .`8888.          8 8888           8.`8888.   Y8
      88 8888               . `88888.              ,8.`8888. ,8.`8888.         8 8888           `8.`8888.
      88 8888              .8. `88888.            ,8'8.`8888,8^8.`8888.        8 888888888888   `8.`8888.
      88 8888             .8`8. `88888.          ,8' `8.`8888' `8.`8888.       8 8888            `8.`8888.
      88 8888   8888888  .8' `8. `88888.        ,8'   `8.`88'   `8.`8888.      8 8888             `8.`8888.
      `8 8888       .8' .8'   `8. `88888.      ,8'     `8.`'     `8.`8888.     8 8888          8b   `8.`8888.
         8888     ,88' .888888888. `88888.    ,8'        `8         `8.`8888.  8 8888          `8b.  ;8.`8888
          `8888888P'  .8'        `8. `88888. ,8'           `         `8.`8888. 8 888888888888   `Y8888P ,88P
"""

GAMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "games"))

def get_metadata(file_path):
    """Scans the game file for __desc__ without importing it."""
    meta = {"desc": "No description available"}
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
    """Displays instructions and author information for the Games Module."""
    print(f"\n{Color.BOLD}--- GAME CENTER HELP ---{Color.RESET}")
    print(f"This module acts as a dynamic launcher for standalone Python games.")
    print(f"1. {Color.GREEN}Listing:{Color.RESET} It scans the '../games/' directory for .py files.")
    print(f"2. {Color.GREEN}Metadata:{Color.RESET} It reads the '__desc__' variable from files automatically.")
    print(f"3. {Color.GREEN}Launching:{Color.RESET} Games are opened in a separate terminal window.")
    
    print(f"\n{Color.YELLOW}Commands:{Color.RESET}")
    print(f" - [ID]: Enter the number to start the game.")
    print(f" - [Name]: Enter the filename (without .py) to start.")
    print(f" - 'help' or '?': Show this information.")
    print(f" - 'q', 'exit', 'quit': Return to the main CLI.")
    
    # Author section at the bottom
    print(f"\n{Color.GRAY}{'-' * 40}")
    print(f"author:  Sebastian Januchowski")
    print(f"email:   polsoft.its@fastservice.com")
    print(f"github:  https://github.com/seb07uk")
    print(f"         2026© polsoft.ITS London{Color.RESET}\n")

@command(name="games", aliases=["play", "g"])
def games_dispatcher(*args):
    """Launcher for games in TERMINAL CLI."""
    
    os.system('cls' if os.name == 'nt' else 'clear')

    if not os.path.exists(GAMES_DIR):
        os.makedirs(GAMES_DIR)

    print(f"{Color.CYAN}{HEADER}{Color.RESET}")
    
    files = [f for f in os.listdir(GAMES_DIR) if f.endswith(".py") and f != "__init__.py"]
    
    if not files:
        print(f"{Color.YELLOW}[!] The /games folder is empty.{Color.RESET}")
        return

    print(f"{Color.BOLD}{'ID':<3} | {'GAME':<20} | {'DESCRIPTION'}{Color.RESET}")
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
        print(f"\n{Color.GRAY}Enter ID/Name, 'help' for info, or 'q' to exit.{Color.RESET}")
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
            print(f"{Color.YELLOW}[*] Launching {game_name} in a new window...{Color.RESET}")
            try:
                subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            except Exception as e:
                print(f"{Color.RED}[ERROR] Could not start game: {e}{Color.RESET}")
        else:
            print(f"{Color.RED}[!] Unknown command or game: {choice}{Color.RESET}")

if __name__ == "__main__":
    games_dispatcher()