# LMBreach

## Introduction

**LMBreach** is an interactive command-line tool designed to test and evaluate the security and robustness of Language Models (LMs). It allows users to load custom modules, payloads, and jailbreaks to simulate various scenarios and analyze the responses of language models.

**Note:** Currently, LMBreach only works with **[LM Studio](https://lmstudio.ai/)** as the LLM host.

## Features

- **Workspace Management**: Create and switch between different workspaces to organize your testing sessions.
- **Module Handling**: Load and execute custom modules tailored for specific testing scenarios.
- **Payload and Jailbreak Integration**: Incorporate diverse payloads and jailbreak scripts to challenge language models.
- **Session Management**: Maintain detailed session information and view comprehensive module data.
- **Customizable API Endpoint**: Configure the HTTP address to connect to your language model API hosted by LM Studio.
- **Interactive CLI**: Navigate and utilize the tool efficiently with an intuitive command-line interface.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/LMBreach.git

# Navigate into the directory
cd LMBreach

# Install dependencies
pip install -r requirements.txt
```

## Usage

**Prerequisite:** Ensure you have **LM Studio** installed and running as your LLM host.

Run the main script to start the interactive session:

```bash
python lmbreach.py
```

Upon starting, you'll see the LMBreach logo and a prompt ready for commands.

### Available Commands

- **use workspace [index/name]**: Switch or create a workspace.
- **use module [index/name]**: Load a module by index or name.
- **use payload [index/name]**: Load a payload by index or name.
- **use jailbreak [index/name]**: Load a jailbreak by index or name.
- **show [workspaces/modules/payloads/jailbreaks]**: Display available items.
- **print notes**: Display notes related to the current workspace.
- **session info**: Show current session information.
- **module info**: Display detailed information about the loaded module.
- **run** or **breach**: Execute the currently loaded module.
- **set var [variable_name] [new_value]**: Set a variable in the loaded module.
- **set http_address [new_address]**: Update the HTTP address for the LM Studio API.
- **help**: Show the help message with available commands.
- **quit**: Exit the program.

### Example Session

```bash
# Start LMBreach
python lmbreach.py

# Create or switch to a workspace
use workspace my_workspace

# Load a module by index or name
use module 1

# Load a payload
use payload default_payload

# Load a jailbreak script
use jailbreak default_jailbreak

# View session information
session info

# Run the loaded module
run
```

### Setting the HTTP Address

By default, LMBreach connects to LM Studio at `http://localhost:1234/v1/chat/completions`. If your LM Studio instance is running on a different address or port, you can change it using:

```bash
set http_address http://your-custom-address:port/path
```

## Modules, Payloads, and Jailbreaks

- **Modules**: Scripts that define specific testing procedures or interactions with the language model.
- **Payloads**: Data or prompts sent to the language model during testing.
- **Jailbreaks**: Scripts designed to test the language model's ability to handle unexpected or adversarial inputs.

## Session Management

LMBreach maintains session information, allowing you to:

- Switch between workspaces without losing progress.
- Keep track of loaded modules, payloads, and jailbreaks.
- View notes and logs associated with each session.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a pull request.

## Disclaimer

LMBreach is intended for ethical testing and evaluation of language models. Please ensure you comply with all applicable laws and regulations when using this tool.

---
