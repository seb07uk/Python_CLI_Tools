import os
from pathlib import Path
from datetime import datetime
from cli import command, Color

__author__ = "Sebastian Januchowski"
__category__ = "io"
__group__ = "core"

@command(name="print", aliases=["cat", "type"])
def print_file(*args):
    """Reading notes / JSON preview / Displaying source code. Logs to History\\print.log"""
    
    # Obsługa pomocy
    if not args or "-h" in args or "--help" in args:
        print(f"{Color.CYAN}Użycie:{Color.RESET}")
        print(f"  print <ścieżka_do_pliku>")
        print(f"  cat <ścieżka_do_pliku>")
        print(f"  type <ścieżka_do_pliku>")
        print(f"\n{Color.CYAN}Opis:{Color.RESET}")
        print("  Wyświetla zawartość pliku w konsoli i zapisuje kopię do logów historii.")
        print(f"  Logi są przechowywane w: %userprofile%\\.polsoft\\psCLI\\History\\print.log")
        return
    
    filepath = args[0]
    path = Path(filepath)
    
    # Konfiguracja ścieżki logowania
    log_dir = Path.home() / ".polsoft" / "psCLI" / "History"
    log_file = log_dir / "print.log"
    
    if not path.exists():
        error_msg = f"[ERROR] Plik {filepath} nie istnieje."
        print(f"{Color.RED}{error_msg}{Color.RESET}")
        return

    try:
        content = path.read_text(encoding="utf-8")
        
        # Wyświetlanie w konsoli
        print(f"{Color.GRAY}--- Content: {filepath} ---{Color.RESET}")
        print(content)
        print(f"{Color.GRAY}--- End of file ---{Color.RESET}")

        # Zapis do print.log
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] Accessed: {filepath}\n")
            f.write(f"{'-'*20}\n{content}\n{'='*40}\n")

    except Exception as e:
        print(f"{Color.RED}Nie można odczytać pliku: {e}{Color.RESET}")