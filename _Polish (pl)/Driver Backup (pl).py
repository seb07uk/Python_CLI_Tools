import os
import subprocess
import sys
import ctypes

def is_admin():
    """Sprawdza, czy skrypt został uruchomiony jako administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def backup_drivers(destination_path):
    """Wykonuje kopię zapasową sterowników przy użyciu narzędzia DISM."""
    
    # Tworzenie folderu docelowego, jeśli nie istnieje
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        print(f"[*] Utworzono folder: {destination_path}")

    print(f"[*] Rozpoczynanie eksportu sterowników do: {destination_path}")
    print("[!] To może potrwać kilka minut...")

    # Komenda DISM do eksportu sterowników
    # /Export-Driver wyciąga sterowniki firm trzecich (OEM) z magazynu sterowników
    cmd = [
        "dism", 
        "/online", 
        "/export-driver", 
        f"/destination:{destination_path}"
    ]

    try:
        # Uruchomienie procesu
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"[+] Sukces! Sterowniki zostały zapisane.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[-] Błąd podczas wykonywania komendy DISM:")
        print(e.stderr)
    except Exception as e:
        print(f"[-] Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    # 1. Sprawdzenie uprawnień
    if not is_admin():
        print("[-] BŁĄD: Musisz uruchomić ten skrypt jako ADMINISTRATOR.")
        # Opcjonalnie: próba wymuszenia restartu z uprawnieniami admina
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        input("Naciśnij Enter, aby zamknąć...")
        sys.exit()

    # 2. Definicja ścieżki (domyślnie folder 'DriverBackup' na pulpicie)
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    backup_folder = os.path.join(desktop, 'DriverBackup')

    # 3. Uruchomienie funkcji
    backup_drivers(backup_folder)
    
    input("\nProces zakończony. Naciśnij Enter, aby wyjść...")