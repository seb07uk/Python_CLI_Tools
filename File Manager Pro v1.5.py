import os
import shutil
import subprocess
import datetime
from pathlib import Path

# Konfiguracja kolorów ANSI
G = "\033[92m"  # Zielony
R = "\033[91m"  # Czerwony
Y = "\033[93m"  # Żółty
B = "\033[94m"  # Niebieski
RESET = "\033[0m"
BOLD = "\033[1m"

class FileManager:
    def __init__(self):
        self.msg = ""
        self.running = True

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_dir_content(self):
        try:
            items = os.listdir('.')
            dirs = sorted([d for d in items if os.path.isdir(d)], key=str.lower)
            files = sorted([f for f in items if os.path.isfile(f)], key=str.lower)
            return dirs, files
        except Exception as e:
            self.msg = f"{R}[!] Błąd odczytu: {e}{RESET}"
            return [], []

    def draw_menu(self):
        self.clear_screen()
        cwd = os.getcwd()
        dirs, files = self.get_dir_content()

        print(f"\n  {Y}DIRECTORY CONTENT:{RESET}  {B}[{cwd}]{RESET}")
        print(f"{B} ┌──────────────────────────────────────────────────────────────────────────────────────────────┐{RESET}")
        
        for d in dirs:
            name = f"  {G}[DIR]{RESET}  {d}"
            print(f"{B} │{RESET} {name:<101} {B}│{RESET}")
        
        if dirs and files:
            print(f"{B} ├──────────────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
            
        for f in files:
            name = f"         {f}"
            print(f"{B} │{RESET} {name:<92} {B}│{RESET}")
            
        print(f"{B} └──────────────────────────────────────────────────────────────────────────────────────────────┘{RESET}\n")
        
        menu_box = [
            "╔═══════════════════════════════════════════════════════════════════════════════════════════════╗",
            "║                                CMD CLI FILE MANAGER PRO (Python)                              ║",
            "╠═══════════════════════════════════════════════════════════════════════════════════════════════╣",
            "║  [1]  REFRESH          [2]  ENTER (CD)       [3]  UP (..)          [4]  DISK INFO             ║",
            "║  [5]  NEW FILE         [6]  NEW FOLDER       [7]  DELETE FILE      [8]  DELETE FOLDER         ║",
            "║  [9]  RENAME           [10] COPY (SHUTIL)    [11] MOVE (SHUTIL)    [12] SAVE LIST             ║",
            "║  [13] BACKUP (MIRR)    [14] SEARCH           [15] OPEN SAVES       [16] HELP                  ║",
            "║  [17] ABOUT            [18] EXIT                                                              ║",
            "╚═══════════════════════════════════════════════════════════════════════════════════════════════╝"
        ]
        for line in menu_box:
            print(f"{B}{line}{RESET}")
        
        if self.msg:
            print(f"\n{self.msg}")
            self.msg = ""

    def run(self):
        # Ustawienie tytułu okna i rozmiaru (Windows)
        if os.name == 'nt':
            os.system("title CMD CLI FILE MANAGER PRO")
            os.system("mode con: cols=105 lines=50")

        while self.running:
            self.draw_menu()
            choice = input(f"\n{B} CMD CLI > {RESET}Select option: ").strip()
            self.handle_choice(choice)

    def handle_choice(self, choice):
        if choice == "1": return
        elif choice == "2": self.enter_dir()
        elif choice == "3": os.chdir("..")
        elif choice == "4": self.disk_info()
        elif choice == "5": self.new_file()
        elif choice == "6": self.new_folder()
        elif choice == "7": self.delete_file()
        elif choice == "8": self.delete_folder()
        elif choice == "9": self.rename_item()
        elif choice == "10": self.copy_item()
        elif choice == "11": self.move_item()
        elif choice == "12": self.save_list()
        elif choice == "13": self.backup_mirror()
        elif choice == "14": self.search_files()
        elif choice == "15": self.open_saves()
        elif choice == "16": self.show_help()
        elif choice == "17": self.show_about()
        elif choice == "18": self.running = False
        else: self.msg = f"{R} [!] Invalid selection!{RESET}"

    # --- AKCJE ---

    def enter_dir(self):
        target = input(" [?] Enter folder: ")
        if os.path.exists(target) and os.path.isdir(target):
            os.chdir(target)
        else:
            self.msg = f"{R} [!] ERROR: Not found!{RESET}"

    def new_file(self):
        name = input(" [+] New file name: ")
        try:
            with open(name, 'a'): os.utime(name, None)
            self.msg = f"{G} [+] Success{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def new_folder(self):
        name = input(" [+] New folder name: ")
        try:
            os.makedirs(name, exist_ok=True)
            self.msg = f"{G} [+] Success{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def delete_file(self):
        name = input(" [!] File to delete: ")
        try:
            os.remove(name)
            self.msg = f"{G} [+] Deleted{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def delete_folder(self):
        name = input(" [!] Folder to delete: ")
        try:
            shutil.rmtree(name)
            self.msg = f"{G} [+] Removed{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def rename_item(self):
        old = input(" [!] Current name: ")
        new = input(" [!] New name: ")
        try:
            os.rename(old, new)
            self.msg = f"{G} [+] Renamed{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def disk_info(self):
        self.clear_screen()
        print(f"\n{B}  ═══ DIRECTORY AND DISK STATISTICS ═══{RESET}\n")
        # W Pythonie używamy shutil.disk_usage
        usage = shutil.disk_usage(os.getcwd())
        print(f"  {Y}[ DISK USAGE ]{RESET}")
        print(f"  Total: {usage.total / (1024**3):.2f} GB")
        print(f"  Used:  {usage.used / (1024**3):.2f} GB")
        print(f"  Free:  {usage.free / (1024**3):.2f} GB\n")
        
        dirs, files = self.get_dir_content()
        total_size = sum(os.path.getsize(f) for f in files)
        print(f"  {Y}[ CONTENT SUMMARY ]{RESET}")
        print(f"  > Total Folders: {len(dirs)}")
        print(f"  > Total Files:   {len(files)}")
        print(f"  > Total Size:    {total_size / (1024**2):.2f} MB\n")
        input("Press Enter to return...")

    def save_list(self):
        target_dir = Path.home() / ".polsoft" / "psCLI" / "FileList"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        folder_name = Path(os.getcwd()).name or "DRIVE"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = target_dir / f"{folder_name}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"FILE LIST - {datetime.datetime.now()}\n")
                f.write(f"LOCATION: {os.getcwd()}\n\n")
                for item in os.listdir('.'):
                    f.write(f"{item}\n")
            self.msg = f"{G} [+] SUCCESS: List saved to {filename.name}!{RESET}"
        except Exception as e:
            self.msg = f"{R} [!] ERROR: {e}{RESET}"

    def search_files(self):
        query = input(" [?] Search query (e.g., .png): ")
        print(f"\n  {Y}SEARCH RESULTS:{RESET}")
        print(f"{B} ┌──────────────────────────────────────────────────────────────────────────────────────────────┐{RESET}")
        count = 0
        for path in Path('.').rglob(f"*{query}*"):
            line = f" {path}"
            print(f"{B} │{RESET} {line[:92]:<92} {B}│{RESET}")
            count += 1
        print(f"{B} └──────────────────────────────────────────────────────────────────────────────────────────────┘{RESET}")
        print(f" Found: {count} items.")
        input("\nPress Enter to return...")

    def show_about(self):
        self.clear_screen()
        about_text = f"""
{B}╔══════════════════════════════════════════════════════════════════════════╗{RESET}
{B}║                                  ABOUT                                   ║{RESET}
{B}╠══════════════════════════════════════════════════════════════════════════╣{RESET}
        
                   {G}CMD CLI File Manager Pro v1.5 (Python Edition){RESET}

                   Author: Sebastian Januchowski
                   Ported to Python for better stability.
        
{B}╚══════════════════════════════════════════════════════════════════════════╝{RESET}
        """
        print(about_text)
        input("Press Enter to return...")

    def open_saves(self):
        target_dir = Path.home() / ".polsoft" / "psCLI" / "FileList"
        target_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(target_dir) if os.name == 'nt' else subprocess.call(['open', str(target_dir)])
        self.msg = f"{G} [+] Opening save folder...{RESET}"

    def show_help(self):
        self.clear_screen()
        print(f"{B}--- HELP SCREEN ---{RESET}\n[1-3] Navigation\n[4] Stats\n[5-8] CRUD operations\n[9-11] File management\n...")
        input("\nPress Enter to return...")

    # Uproszczone funkcje kopiowania dla przykładu
    def copy_item(self):
        src = input(" [?] Source: ")
        dst = input(" [?] Destination: ")
        try:
            if os.path.isdir(src): shutil.copytree(src, dst)
            else: shutil.copy2(src, dst)
            self.msg = f"{G} [+] Copy finished.{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def move_item(self):
        src = input(" [?] Source: ")
        dst = input(" [?] Destination: ")
        try:
            shutil.move(src, dst)
            self.msg = f"{G} [+] Move finished.{RESET}"
        except Exception as e: self.msg = f"{R} [!] Error: {e}{RESET}"

    def backup_mirror(self):
        src = input(" [?] Source: ")
        dst = input(" [?] Destination: ")
        # W Pythonie mirror można symulować przez usunięcie celu i ponowne copytree 
        # lub użycie zewnętrznego narzędzia robocopy przez subprocess
        if os.name == 'nt':
            subprocess.run(['robocopy', src, dst, '/mir'])
            self.msg = f"{G} [+] Mirror Backup completed (via Robocopy).{RESET}"
        else:
            self.msg = f"{R} [!] Mirroring available only on Windows.{RESET}"

if __name__ == "__main__":
    app = FileManager()
    app.run()