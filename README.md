```
 _    ___  ________                     _     
| |   |  \/  | ___ \                   | |    
| |   | .  . | |_/ /_ __ ___  __ _  ___| |__  
| |   | |\/| | ___ \ '__/ _ \/ _` |/ __| '_ \ 
| |___| |  | | |_/ / | |  __/ (_| | (__| | | |
\_____|_|  |_|____/|_|  \___|\__,_|\___|_| |_|
```

# LMBreach

> **A modular security testing framework for Language Models**

## 🎯 Overview

**LMBreach** is an interactive command-line tool designed for AI agents and developers to systematically test and evaluate the security, robustness, and behavioral boundaries of Language Models. Built with modularity at its core, LMBreach provides a flexible framework for conducting prompt injection tests, denial-of-service detection, jailbreak attempts, and custom security assessments.

**Current LLM Host Support:** [LM Studio](https://lmstudio.ai/) (extensible architecture for future providers)

## ✨ Key Features

### 🔧 **Modular Architecture**
- **Custom Module System**: Create and load specialized testing modules with minimal boilerplate
- **Payload Integration**: Incorporate diverse attack vectors and test cases from text files
- **Dynamic Loading**: Import and execute modules at runtime without restarting sessions

### 📊 **Workspace Management**
- **Isolated Environments**: Organize testing sessions in separate workspaces
- **Persistent Results**: Automatically track and store test results in CSV format
- **Session State**: Maintain context across multiple testing iterations

### 🎮 **Interactive CLI**
- **Intuitive Commands**: Simple, memorable command structure
- **Real-time Feedback**: Color-coded output for success, warnings, and errors
- **Variable Customization**: Modify module parameters on-the-fly without editing code

### 🔌 **Flexible API Integration**
- **Configurable Endpoints**: Point to any LM Studio instance
- **Standard OpenAI Format**: Uses `/v1/chat/completions` endpoint
- **Easy Migration Path**: Architecture ready for multiple LLM provider support

## 📚 Documentation

- **[Installation Guide](INSTALL.md)** - Prerequisites, setup, and troubleshooting
- **[Cookbook](COOKBOOK.md)** - Practical examples, module development, and best practices
- **[Architecture Overview](ARCHITECTURE.md)** - System design and component interaction
- **[Module Development Guide](MODULE_DEVELOPMENT.md)** - API specification and developer reference

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/brzewVCE/LMBreach.git
cd LMBreach

# Install dependencies
pip install -r requirements.txt

# Ensure LM Studio is running on localhost:1234

# Launch LMBreach
python lmbreach.py
```

### First Session Example

```bash
# Create a new workspace for your testing session
use workspace security_test

# List available modules
show modules

# Load the connection test module
use module 1

# Verify the module configuration
module info

# Execute the test
run

# View results
print notes
```

## 🧩 Module System

LMBreach comes with built-in modules for common security testing scenarios:

| Module | Description | Payload Required |
|--------|-------------|------------------|
| **check_connection** | Verify API connectivity and basic response | ❌ No |
| **prompt_injection** | Test prompt injection vulnerabilities | ✅ Yes |
| **model_DOS** | Detect denial-of-service susceptibility | ✅ Yes |

**Creating custom modules** is straightforward - see [MODULE_DEVELOPMENT.md](MODULE_DEVELOPMENT.md) for the complete guide.

## 💾 Workspace & Results

Every workspace maintains its own CSV database tracking:
- ✅ Success/failure status
- 📝 Module used
- 🎯 Payload applied
- 📊 Detailed notes and responses

Results are automatically organized with successful breaches listed first for easy analysis.

## 🎛️ Command Reference

| Command | Description |
|---------|-------------|
| `use workspace [name]` | Create or switch to a workspace |
| `use module [index\|name]` | Load a testing module |
| `use payload [index\|name]` | Load a payload file |
| `show [workspaces\|modules\|payloads]` | List available items |
| `session info` | Display current session state |
| `module info` | Show loaded module details |
| `run` or `breach` | Execute the loaded module |
| `run [N]` | Execute module N times |
| `set var [name] [value]` | Update module variables |
| `set http_address [url]` | Change API endpoint |
| `print notes` | Display workspace results |
| `help` | Show command help |
| `quit` | Exit LMBreach |

## 🔍 Example Use Cases

### Prompt Injection Testing
```bash
use workspace prompt_injection_tests
use module prompt_injection
use payload info_enum
run
```

### DoS Vulnerability Assessment
```bash
use workspace dos_testing
use module model_DOS
set var timeout 30
use payload unwanted_values
run 5  # Run 5 iterations
```

### Custom Module Development
```bash
# See COOKBOOK.md for step-by-step guide
# See MODULE_DEVELOPMENT.md for API reference
```

## 🏗️ Project Structure

```
LMBreach/
├── lmbreach.py           # Main CLI interface
├── module_handler.py     # Dynamic module loading & execution
├── db_handler.py         # Workspace & result management
├── output_handler.py     # Colored terminal output
├── modules/              # Testing modules
│   ├── check_connection.py
│   ├── prompt_injection.py
│   └── model_DOS.py
├── payloads/             # Attack vectors & test data
│   ├── info_enum.txt
│   ├── misinformation.txt
│   └── unwanted_values.txt
└── workspaces/           # Session databases (CSV files)
```

## 🤝 Contributing

LMBreach is designed to be extended by the community. Contributions are welcome in the form of:

- **New Modules**: Additional testing scenarios and attack vectors
- **Payload Collections**: Curated test cases for specific vulnerabilities
- **Provider Support**: Integration with additional LLM hosting platforms
- **Documentation**: Examples, tutorials, and use case studies

**Contribution Process:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add: description'`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

## ⚖️ License & Ethics

**License:** MIT License - See [LICENSE](LICENSE) file for details

### Responsible Use Guidelines

LMBreach is designed for **ethical security research and testing** purposes only. Users must:

- ✅ Only test language models you own or have explicit permission to test
- ✅ Comply with all applicable laws, regulations, and terms of service
- ✅ Use findings to improve model security and robustness
- ✅ Practice responsible disclosure for discovered vulnerabilities

- ❌ Do not use for malicious purposes
- ❌ Do not test models without authorization
- ❌ Do not weaponize findings or create harmful content

**The developers of LMBreach assume no liability for misuse of this tool.**

## 🙏 Acknowledgments

Built for AI agents and developers exploring the frontiers of language model security.

---

**Version:** 1.0.0 | **Last Updated:** October 2025
