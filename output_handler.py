import colorama
from colorama import Fore, Style
import csv

# Initialize colorama
colorama.init(autoreset=True)

def colored(text, color="default"):
    # Define color mappings using colorama
    colors = {
        "default": Fore.RESET,
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "light_gray": Fore.LIGHTBLACK_EX,
        "light_red": Fore.LIGHTRED_EX,
        "light_green": Fore.LIGHTGREEN_EX,
        "light_yellow": Fore.LIGHTYELLOW_EX,
        "light_blue": Fore.LIGHTBLUE_EX,
        "light_magenta": Fore.LIGHTMAGENTA_EX,
        "light_cyan": Fore.LIGHTCYAN_EX
    }
    
    # Get the selected color code, or default if not found
    color_code = colors.get(color, colors["default"])
    
    # Return the colored text
    return f"{color_code}{text}{Style.RESET_ALL}"

def logo():
    art = """
     _    ___  ________                     _     
    | |   |  \/  | ___ \                   | |    
    | |   | .  . | |_/ /_ __ ___  __ _  ___| |__  
    | |   | |\/| | ___ \ '__/ _ \/ _` |/ __| '_ \ 
    | |___| |  | | |_/ / | |  __/ (_| | (__| | | |
    \_____|_|  |_|____/|_|  \___|\__,_|\___|_| |_|
                                                       
    """
    print(colored(art, "red"))

def warning(message):
    # Print the warning message with only the "icon" in red
    icon = colored("[-]", "red")
    print(f"{icon} {message}")

def info(message):
    # Print the info message with only the "icon" in blue
    icon = colored("[*]", "blue")
    print(f"{icon} {message}")

def success(message):
    # Print the success message with only the "icon" in green
    icon = colored("[+]", "green")
    print(f"{icon} {message}")

def index(index, filename):
    # Print the index and filename in cyan
    index = colored(f"[{index}]", "cyan")
    print(f"{index} {filename}")

def notes(csv_filename):
        """Reads the CSV file and prints entries with colored categories."""
        try:
            with open(csv_filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    status = row.get('success')
                    breach_filename = row.get('breach_filename', 'N/A')
                    payload = row.get('payload', 'N/A')
                    note = row.get('note', 'N/A')

                    # Build the colored message
                    colored_breach_filename = colored(f"File: ", "blue")+colored(f"{breach_filename}")
                    if payload:
                        colored_payload = colored(f"Payload: ", "light_green")+colored(f"{payload}")
                    else:
                        colored_payload = ""
                    colored_note = colored(f"Note: ", "cyan")+colored(f"{note}")

                    # Assemble full message
                    message = f"{colored_breach_filename} {colored_payload} {colored_note}"

                    # Output with success or warning icon
                    if status == 'True':  # Successful case
                        icon = colored("[+]", "green")
                        print(f"{icon} {message}")
                    elif status == 'False':  # Failed case
                        icon = colored("[-]", "red")
                        print(f"{icon} {message}")
                    else:
                        print(f"[?] Invalid status for entry: {message}")
        except FileNotFoundError:
            print(f"File {csv_filename} not found.")

if __name__ == "__main__":
    logo()
    warning("Error message")
    info("Info message")
    success("Success message")
    index(1, "file1.txt")
    notes("./workspaces/Gemini.csv")
