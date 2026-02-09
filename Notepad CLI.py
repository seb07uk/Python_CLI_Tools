import os
import sys
import time
import msvcrt
from datetime import datetime
from colorama import init, Fore, Style

# Inicjalizacja kolorów
init(autoreset=True)

# Definicje kolorów i ścieżek [cite: 32]
green = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
blue = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
target_dir = os.path.join(os.environ['USERPROFILE'], '.polsoft', 'psCLI', 'Notepad')

# Tworzenie katalogu, jeśli nie istnieje [cite: 32]
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{blue}================================{reset}")
    print("          Notepad CLI")
    print(f"{blue}================================{reset}")
    print(f"[1] {green}New Note (Auto-Save){reset}")
    print(f"[2] {blue}Browse Notes (W/S/O){reset}")
    print(f"[3] {yellow}About Author{reset}")
    print(f"[4] {red}Exit{reset}")
    print(f"{blue}================================{reset}")
    print("Selection: ", end='', flush=True)

def new_auto_note():
    os.system('cls')
    print(f"{green}Type your note content.{reset}")
    print(f"{yellow}(Press CTRL+Z then ENTER on a new line to save and finish){reset}")
    print("-" * 32)
    
    lines = []
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            lines.append(line)
    except EOFError:
        pass

    if not lines:
        print(f"{red}[!] Cancelled or empty.{reset}")
        time.sleep(2)
        return

    # Generowanie znacznika czasu i zapis [cite: 33, 34]
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    file_name = f"Note_{ts}.txt"
    full_path = os.path.join(target_dir, file_name)

    with open(full_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n{green}[OK] Saved automatically as: {file_name}{reset}")
    time.sleep(2)

def browse_notes():
    selected = 0
    while True:
        # Odświeżanie listy plików [cite: 35]
        files = [f for f in os.listdir(target_dir) if f.endswith('.txt')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(target_dir, x)), reverse=True)

        if not files:
            os.system('cls')
            print(f"{red}[!] No notes found.{reset}")
            time.sleep(2)
            break

        os.system('cls')
        print(f"{blue}--- NOTE LIST (W/S - Select, O - Open, Q - Back) ---{reset}\n")
        
        for i, file in enumerate(files):
            if i == selected:
                print(f" {green}> {file} {reset}") # [cite: 35]
            else:
                print(f"   {file}")
        
        print("\n")
        
        # Obsługa nawigacji klawiszami 
        key = msvcrt.getch().decode('utf-8').lower()

        if key == 'q':
            break
        elif key == 'w':
            if selected > 0: selected -= 1
        elif key == 's':
            if selected < len(files) - 1: selected += 1
        elif key == 'o':
            # Otwieranie notatki [cite: 37]
            current_file = files[selected]
            os.system('cls')
            print(f"{yellow}File: {current_file}{reset}")
            print(f"{blue}--------------------------------{reset}")
            with open(os.path.join(target_dir, current_file), 'r', encoding='utf-8') as f:
                print(f.read())
            print(f"{blue}--------------------------------{reset}")
            print("Press any key to return to list...")
            msvcrt.getch()

def show_about():
    os.system('cls')
    print(f"{blue}==================================={reset}")
    print("          ABOUT AUTHOR")
    print(f"{blue}==================================={reset}\n")
    print(f"{green}Author:{reset} Sebastian Januchowski [cite: 38]")
    print(f"{green}Email:{reset}  polsoft.its@fastservice.com [cite: 38]")
    print(f"{green}GitHub:{reset} https://github.com/seb07uk [cite: 38]\n")
    print(f"{blue}==================================={reset}\n")
    print("Press any key to return to menu... [cite: 39]")
    msvcrt.getch()

def main():
    while True:
        show_menu()
        
        # Pobieranie klawisza w menu głównym (automatyczne menu)
        choice = msvcrt.getch().decode('utf-8').lower()

        if choice == '1':
            new_auto_note()
        elif choice == '2':
            browse_notes()
        elif choice == '3':
            show_about()
        elif choice == '4':
            print(f"\n{yellow}Closing...{reset}")
            time.sleep(1)
            sys.exit()

if __name__ == "__main__":
    main()