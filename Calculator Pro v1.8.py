import os
import math
import sys
from datetime import datetime

# ==============================================================================
# PATH CONFIGURATION (According to polsoft guidelines)
# ==============================================================================
HIST_DIR = os.path.join(os.environ["USERPROFILE"], ".polsoft", "psCli", "Calculator")
HIST_FILE = os.path.join(HIST_DIR, "history.txt")

# Create history folder if it doesn't exist
if not os.path.exists(HIST_DIR):
    os.makedirs(HIST_DIR)

# ==============================================================================
# ANSI COLORS AND FORMATTING
# ==============================================================================
C = {
    "RES": "\033[0m",
    "RED": "\033[31m",
    "GRN": "\033[32m",
    "YLW": "\033[33m",
    "BLU": "\033[34m",
    "CYN": "\033[36m",
    "GRY": "\033[90m",
    "B": "\033[1m",
    "I": "\033[3m"
}

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def save_history(operation, result):
    """Saves the result to %userprofile%\\.polsoft\\psCli\\Calculator\\history.txt"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {operation} = {result}\n")
    except Exception as e:
        print(f"{C['RED']}History save error: {e}{C['RES']}")

def get_num(prompt_text):
    """Gets a number and converts comma to dot"""
    try:
        val = input(prompt_text).replace(",", ".")
        return float(val)
    except ValueError:
        return None

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ==============================================================================
# FUNCTIONAL MODULES
# ==============================================================================
def show_help():
    clear()
    print(f"{C['CYN']}=== CALCULATOR PRO HELP ==={C['RES']}")
    print(f"{C['GRY']}==========================================={C['RES']}")
    print(f"\n{C['YLW']}OPERATIONS:{C['RES']}")
    print("  - Standard: +, -, *, /")
    print("  - Advanced: Power, Square Root")
    print("  - Trig: Sin, Cos, Tan (provide degrees)")
    print(f"\n{C['YLW']}HISTORY:{C['RES']}")
    print(f"  Path: {C['GRY']}{HIST_FILE}{C['RES']}")
    print(f"\n{C['YLW']}AUTHOR:{C['RES']}")
    print("  Sebastian Januchowski (polsoft.its)")
    print(f"{C['GRY']}==========================================={C['RES']}")
    input("\nPress Enter...")

def show_history():
    clear()
    print(f"{C['BLU']}=== Calculator History ==={C['RES']}")
    print(f"Log: {HIST_FILE}\n")
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Show last 20 entries
            if not lines:
                print("No entries found.")
            for line in lines[-20:]:
                print(line.strip())
    else:
        print("No history file found.")
    input(f"\n{C['GRY']}Press Enter...{C['RES']}")

# ==============================================================================
# MAIN PROGRAM LOOP
# ==============================================================================
def run_calculator():
    os.system('') # Enable ANSI in Windows CMD
    
    while True:
        clear()
        print(f" {C['I']}2026(c) Sebastian Januchowski{C['RES']}")
        print(f"{C['GRN']}==============================={C['RES']}")
        print(f"      {C['CYN']}{C['B']}Calculator Pro v1.8{C['RES']}")
        print(f"{C['GRN']}==============================={C['RES']}\n")
        print(f"[1] {C['YLW']}Addition{C['RES']}      [6] {C['YLW']}Square Root{C['RES']}")
        print(f"[2] {C['YLW']}Subtraction{C['RES']}   [7] {C['YLW']}Sinus{C['RES']}")
        print(f"[3] {C['YLW']}Multiplication{C['RES']}[8] {C['YLW']}Cosinus{C['RES']}")
        print(f"[4] {C['YLW']}Division{C['RES']}      [9] {C['YLW']}Tangens{C['RES']}")
        print(f"[5] {C['YLW']}Power{C['RES']}")
        print(f"\n[h] {C['CYN']}History{C['RES']}    [?] {C['CYN']}Help{C['RES']}    [e] {C['RED']}Exit{C['RES']}\n")

        choice = input("Select: ").lower()

        if choice == 'e':
            user = os.environ.get("USERNAME", "User")
            print(f"\nGoodbye, {C['GRN']}{C['B']}{user}{C['RES']}!")
            break
        elif choice == '?':
            show_help()
        elif choice == 'h':
            show_history()
        elif choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            # Arithmetic operations
            if choice in ['1', '2', '3', '4', '5']:
                a = get_num("First number: ")
                b = get_num("Second number: ")
                if a is None or b is None:
                    print(f"{C['RED']}Data error!{C['RES']}")
                else:
                    if choice == '1': res, op = a + b, f"{a} + {b}"
                    if choice == '2': res, op = a - b, f"{a} - {b}"
                    if choice == '3': res, op = a * b, f"{a} * {b}"
                    if choice == '4':
                        if b == 0:
                            print(f"{C['RED']}Division by zero!{C['RES']}")
                            input()
                            continue
                        res, op = a / b, f"{a} / {b}"
                    if choice == '5': res, op = math.pow(a, b), f"{a} ^ {b}"
                    
                    print(f"{C['GRN']}Result: {C['B']}{res}{C['RES']}")
                    save_history(op, res)
            
            # Square root
            elif choice == '6':
                a = get_num("Number: ")
                if a is not None and a >= 0:
                    res = math.sqrt(a)
                    print(f"{C['GRN']}Result: {C['B']}{res}{C['RES']}")
                    save_history(f"sqrt({a})", res)
                else:
                    print(f"{C['RED']}Error (negative number or invalid data)!{C['RES']}")
            
            # Trigonometry
            elif choice in ['7', '8', '9']:
                deg = get_num("Angle (degrees): ")
                if deg is not None:
                    rad = math.radians(deg)
                    if choice == '7': res, func = math.sin(rad), "sin"
                    if choice == '8': res, func = math.cos(rad), "cos"
                    if choice == '9': res, func = math.tan(rad), "tan"
                    print(f"{C['GRN']}{func}({deg}) = {C['B']}{res}{C['RES']}")
                    save_history(f"{func}({deg})", res)
            
            input("\nEnter...")

if __name__ == "__main__":
    run_calculator()