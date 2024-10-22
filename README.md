# LMBreach

LMBreach is a command-line tool designed for security researchers and developers to test the robustness and security of language models (LMs) by executing custom modules and payloads. It provides an interactive shell to manage workspaces, modules, and payloads, and to execute breach modules against language models.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
  - [Commands](#commands)
  - [Example Session](#example-session)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Features

- **Workspace Management**: Organize your breach tests using multiple workspaces.
- **Module and Payload Loading**: Load and execute custom breach modules and payloads.
- **Interactive CLI**: User-friendly command-line interface with helpful commands and color-coded outputs.
- **Session Logging**: Logs breach attempts and results for analysis.
- **Customizable Settings**: Configure variables and HTTP addresses for modules.

## Installation

### Prerequisites

- **Python 3.7** or higher
- **Git** (optional, for cloning the repository)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/LMBreach.git
   ```

   *Replace `yourusername` with the actual GitHub username. Alternatively, you can download the ZIP file from GitHub and extract it.*

2. **Navigate to the Project Directory**

   ```bash
   cd LMBreach
   ```

3. **Install Required Python Packages**

   LMBreach uses standard Python libraries. If any external dependencies are added in the future, install them using:

   ```bash
   pip install -r requirements.txt
   ```

   *Currently, there is no `requirements.txt` file as there are no external dependencies.*

## Usage

Run the main script to start the interactive shell:

```bash
python main.py
```

### Commands

Use the following commands within the LMBreach interactive shell:

- **`use workspace [index/name]`**: Switch to or create a workspace.
- **`use module [index/name]`**: Load a breach module by index or name.
- **`use payload [index/name]`**: Load a payload by index or name.
- **`show [workspaces/modules/payloads]`**: Display available workspaces, modules, or payloads.
- **`print notes`**: Display notes related to the current workspace.
- **`session info`**: Show information about the current session.
- **`module info`**: Show detailed information about the currently loaded module.
- **`run` or **`breach`**: Execute the currently loaded module.
- **`set var [variable_name] [new_value]`**: Set a variable in the loaded module.
- **`set http_address [new_address]`**: Set a new HTTP address for the API.
- **`help`**: Display the help message with available commands.
- **`quit`**: Exit the program.

### Example Session

1. **Start LMBreach**

   ```bash
   python main.py
   ```

2. **Display Help**

   ```plaintext
   > help
   ```

3. **Create or Switch to a Workspace**

   ```plaintext
   > use workspace my_workspace
   ```

   *This will create a new workspace named `my_workspace` or switch to it if it already exists.*

4. **Show Available Modules**

   ```plaintext
   my_workspace > None > None: show modules
   ```

5. **Load a Module**

   ```plaintext
   my_workspace > None > None: use module 1
   ```

   *You can also use the module name instead of the index:*

   ```plaintext
   my_workspace > None > None: use module my_module
   ```

6. **Show Available Payloads**

   ```plaintext
   my_workspace > my_module > None: show payloads
   ```

7. **Load a Payload**

   ```plaintext
   my_workspace > my_module > None: use payload 1
   ```

   *Or by name:*

   ```plaintext
   my_workspace > my_module > None: use payload my_payload
   ```

8. **Set Module Variables**

   ```plaintext
   my_workspace > my_module > my_payload: set var timeout 30
   ```

9. **Set HTTP Address**

   ```plaintext
   my_workspace > my_module > my_payload: set http_address http://localhost:8000/v1/chat/completions
   ```

10. **Execute the Module**

    ```plaintext
    my_workspace > my_module > my_payload: run
    ```

11. **View Session Information**

    ```plaintext
    my_workspace > my_module > my_payload: session info
    ```

12. **Print Notes**

    ```plaintext
    my_workspace > my_module > my_payload: print notes
    ```

13. **Exit LMBreach**

    ```plaintext
    my_workspace > my_module > my_payload: quit
    ```

## Directory Structure

The project directories are organized as follows:

- **`modules/`**: Contains breach modules. Each module is a script or file that defines a breach test.
- **`payloads/`**: Contains payloads used by modules during execution.
- **`workspaces/`**: Contains workspaces and their respective logs in CSV format. Each workspace has its own CSV file for logging breach attempts and results.
- **`main.py`**: The main script to run LMBreach.
- **`db_handler.py`**: Handles database operations for workspaces, modules, and payloads.
- **`module_handler.py`**: Manages loading and execution of breach modules.
- **`output_handler.py`**: Provides colored output and logging functionalities.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button at the top right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/LMBreach.git
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Commit Your Changes**

   ```bash
   git commit -am "Add new feature"
   ```

5. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

   Go to the original repository and click on "Pull Requests" to submit your changes for review.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Disclaimer

LMBreach is intended for educational and ethical testing purposes only. Unauthorized or malicious use against systems without explicit permission is illegal and unethical. The developers are not responsible for any misuse of this tool.

**Use responsibly and always ensure you have proper authorization before conducting any tests.**

---

*Note: LMBreach is currently under development. Features and functionalities are subject to change. For any issues or suggestions, please open an [issue](https://github.com/yourusername/LMBreach/issues) on GitHub.*