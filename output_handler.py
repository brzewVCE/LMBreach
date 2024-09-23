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
    
    # Print the colored text
    print(f"{color_code}{text}{Style.RESET_ALL}")

def logo():
    art = """
     _     _    ___  ________                     _     
    | |   | |   |  \/  | ___ \                   | |    
    | |   | |   | .  . | |_/ /_ __ ___  __ _  ___| |__  
    | |   | |   | |\/| | ___ \ '__/ _ \/ _` |/ __| '_ \ 
    | |___| |___| |  | | |_/ / | |  __/ (_| | (__| | | |
    \_____|_____|_|  |_|____/|_|  \___|\__,_|\___|_| |_|
                                                       
    """
    colored(art, "red")
    
                                                    
def warning(message):
    # Print the warning message in red
    warning_message = colored(f"[W]: {message}", "red")
    
def info(message):
    # Print the info message in green
    info_message = colored(f"[I]: {message}")

def success(message):
    # Print the success message in green
    success_message = colored(f"[S]: {message}", "green")



    

if __name__ == "__main__":
    logo()
    warning("Error message")
    info("Info message")
    success("Success message")