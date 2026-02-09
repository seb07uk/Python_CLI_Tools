import os
import sys
import time
import msvcrt
from datetime import datetime
from colorama import init, Fore, Style

# Inicjalizacja kolorów
init(autoreset=True)

# Konfiguracja ścieżek 
base_dir = os.path.join(os.environ['USERPROFILE'], '.polsoft', 'psCLI', 'Notepad')
trash_dir = os.path.join(base_dir, '.trash')
for d in [base_dir, trash_dir]:
    if not os.name == 'nt': continue # Zabezpieczenie dla Windows
    if not os.path.exists(d): os.makedirs(d)

# Słownik tłumaczeń
LANGS = {
    'en': {
        'title': 'NOTEPAD CLI ULTRA v4.0',
        'm1': '[1] New Note (Auto-Save)',
        'm2': '[2] Library (W/S/O/E/D/H)',
        'm3': '[3] Search Notes',
        'm4': '[4] Empty Trash',
        'm5': '[5] About Author',
        'm6': '[L] Change Language (Current: EN)',
        'mQ': '[Q] Exit',
        'select': 'Selection: ',
        'no_notes': '[!] No notes found.',
        'search_prompt': 'Enter search term: ',
        'enc_prompt': 'Encrypt with password? (Leave empty for NO): ',
        'pass_prompt': 'Locked! Enter password: ',
        'save_ok': '[OK] Saved: ',
        'trash_ok': 'Trash emptied!',
        'nav': 'NAV | W/S: Up/Down | O: Open | E: Edit | D: Trash | H: HTML | Q: Back',
        'stats': 'Lines: {} | Words: {}',
        'any_key': 'Press any key to return...',
        'editor_info': 'Type content. Press CTRL+Z then ENTER to save.'
    },
    'pl': {
        'title': 'NOTEPAD CLI ULTRA v4.0',
        'm1': '[1] Nowa notatka (Auto-Zapis)',
        'm2': '[2] Biblioteka (W/S/O/E/D/H)',
        'm3': '[3] Szukaj notatek',
        'm4': '[4] Oproznij kosz',
        'm5': '[5] O autorze',
        'm6': '[L] Zmien jezyk (Obecny: PL)',
        'mQ': '[Q] Wyjscie',
        'select': 'Wybor: ',
        'no_notes': '[!] Nie znaleziono notatek.',
        'search_prompt': 'Wpisz fraze: ',
        'enc_prompt': 'Zaszyfrowac haslem? (Puste = NIE): ',
        'pass_prompt': 'Zablokowane! Podaj haslo: ',
        'save_ok': '[OK] Zapisano: ',
        'trash_ok': 'Kosz oprozniony!',
        'nav': 'NAWIGACJA | W/S: Gora/Dol | O: Otworz | E: Edytuj | D: Kosz | H: HTML | Q: Powrot',
        'stats': 'Linii: {} | Slow: {}',
        'any_key': 'Nacisnij dowolny klawisz, aby wrocic...',
        'editor_info': 'Wpisz tresc. Nacisnij CTRL+Z i ENTER, aby zapisac.'
    }
}

current_lang = 'en' # Startowy język: EN 

def simple_cipher(text, key):
    result = ""
    for i, char in enumerate(text):
        result += chr(ord(char) ^ ord(key[i % len(key)]))
    return result

def get_t(key):
    return LANGS[current_lang].get(key, key)

def show_menu():
    os.system('cls')
    b, g, c, y, r = Fore.BLUE, Fore.GREEN, Fore.CYAN, Fore.YELLOW, Fore.RED
    print(f"{b}================================================")
    print(f"          {get_t('title')}")
    print(f"{b}================================================")
    print(f" {get_t('m1')}")
    print(f" {get_t('m2')}")
    print(f" {get_t('m3')}")
    print(f" {get_t('m4')}")
    print(f" {get_t('m5')}")
    print(f" {Fore.MAGENTA}{get_t('m6')}")
    print(f" {get_t('mQ')}")
    print(f"{b}================================================")
    print(f"{get_t('select')}", end='', flush=True)

def new_note(existing_content="", filename=None):
    os.system('cls')
    print(f"{Fore.GREEN}--- EDITOR ---{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{get_t('editor_info')}{Style.RESET_ALL}\n" + "-"*40)
    
    lines = sys.stdin.readlines()
    if not lines and not existing_content: return

    encrypt = input(f"\n{get_t('enc_prompt')}")
    final_text = "".join(lines)
    if encrypt:
        final_text = "ENCRYPTED:" + simple_cipher(final_text, encrypt)

    if not filename:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Note_{ts}.txt"
    
    with open(os.path.join(base_dir, filename), 'w', encoding='utf-8') as f:
        f.write(final_text)
    print(f"\n{get_t('save_ok')}{filename}")
    time.sleep(1.5)

def browse(query=""):
    sel = 0
    while True:
        files = [f for f in os.listdir(base_dir) if f.endswith('.txt') and query.lower() in f.lower()]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(base_dir, x)), reverse=True)

        if not files:
            print(f"\n{get_t('no_notes')}")
            time.sleep(1.5); break

        os.system('cls')
        print(f"{Fore.BLUE}{get_t('nav')}{Style.RESET_ALL}")
        print("-" * 75)
        for i, f in enumerate(files):
            print(f"{Fore.GREEN if i==sel else ''}{'> ' if i==sel else '  '}{f}{Style.RESET_ALL}")

        key = msvcrt.getch().decode('utf-8').lower()
        path = os.path.join(base_dir, files[sel])

        if key == 'q': break
        elif key == 'w' and sel > 0: sel -= 1
        elif key == 's' and sel < len(files)-1: sel += 1
        elif key == 'd':
            os.rename(path, os.path.join(trash_dir, files[sel]))
            if sel > 0: sel -= 1
        elif key == 'h':
            with open(path, 'r', encoding='utf-8') as f: data = f.read()
            h_path = path.replace('.txt', '.html')
            with open(h_path, 'w', encoding='utf-8') as f:
                f.write(f"<html><body style='background:#121212;color:#eee;padding:20px;'><pre>{data}</pre></body></html>")
            print("\nHTML Export OK!"); time.sleep(1)
        elif key == 'o' or key == 'e':
            with open(path, 'r', encoding='utf-8') as f: data = f.read()
            if data.startswith("ENCRYPTED:"):
                pw = input(f"\n{get_t('pass_prompt')}")
                data = simple_cipher(data[10:], pw)
            
            if key == 'o':
                os.system('cls')
                print(f"{data}\n\n{Fore.BLUE}" + "-"*30)
                print(get_t('stats').format(len(data.splitlines()), len(data.split())))
                print(get_t('any_key'))
                msvcrt.getch()
            else:
                new_note(existing_content=data, filename=files[sel])

def main():
    global current_lang
    while True:
        show_menu()
        c = msvcrt.getch().decode('utf-8').lower()

        if c == '1': new_note()
        elif c == '2': browse()
        elif c == '3': browse(input(f"\n{get_t('search_prompt')}"))
        elif c == '4':
            for f in os.listdir(trash_dir): os.remove(os.path.join(trash_dir, f))
            print(f"\n{get_t('trash_ok')}"); time.sleep(1)
        elif c == '5':
            os.system('cls')
            print(f"Author: Sebastian Januchowski [cite: 38]\nGitHub: https://github.com/seb07uk [cite: 38]")
            msvcrt.getch()
        elif c == 'l':
            current_lang = 'pl' if current_lang == 'en' else 'en'
        elif c == 'q':
            sys.exit()

if __name__ == "__main__":
    main()