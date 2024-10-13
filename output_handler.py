import colorama
from colorama import Fore, Style

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
    # Print the index and filename in light blue
    index = colored(f"[{index}]", "light_blue")
    print(f"{index} {filename}")

if __name__ == "__main__":
    logo()
    warning("Error message")
    info("Info message")
    success("Success message")
    index(1, "file1.txt")
