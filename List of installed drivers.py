import subprocess
import os

# Inicjalizacja kolorów ANSI (standard w nowoczesnych terminalach)
class Colors:
    HEADER = '\033[2;3m'
    YELLOW = '\033[33m'
    CYAN = '\033[6m'
    INVERSE_ITALIC = '\033[7;3m'
    RESET = '\033[0m'

def list_drivers():
    # Ustawienie tytułu okna (działa na Windows)
    os.system("title List of installed drivers by polsoft.ITS")

    # Nagłówek skryptu [cite: 1]
    author_info = f"{Colors.HEADER}Written by Sebastian Januchowski                  polsoft.ITS                   e-mail: polsoft.its@fastservice.com{Colors.RESET}"
    
    print(author_info)
    print("\n")
    print(f"                                             {Colors.INVERSE_ITALIC}↓ List of  Installed Drivers  ↓{Colors.RESET}")
    print("\n")

    # Wywołanie komendy driverquery 
    print(Colors.YELLOW)
    try:
        # Wykonanie komendy i wyświetlenie wyniku bezpośrednio w konsoli
        subprocess.run(["driverquery"], check=True)
    except FileNotFoundError:
        print("Błąd: Komenda 'driverquery' nie została znaleziona w systemie.")
    print(Colors.RESET)

    print("\n")
    print(f"                                             {Colors.INVERSE_ITALIC}↑ List of  Installed Drivers  ↑{Colors.RESET}")
    print("\n")

    # Stopka i pauza [cite: 4, 5]
    print(f"{Colors.CYAN}press any key to continue . . .{Colors.RESET}")
    print("\n")
    print(author_info)
    
    # Symulacja "pause >nul"
    input()

if __name__ == "__main__":
    list_drivers()