# Architecture Overview

> **Understanding LMBreach's design, components, and data flow**

This document provides a technical overview of LMBreach's architecture, designed to help AI agents and developers understand how the system works internally.

## 🏗️ System Design Philosophy

LMBreach follows these core principles:

1. **Modularity**: Testing logic is isolated in independent modules
2. **Simplicity**: Minimal dependencies, straightforward data flow
3. **Extensibility**: Easy to add new modules, payloads, and features
4. **Transparency**: Clear data structures, readable code
5. **AI-Friendly**: Designed for programmatic control and automation

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interface                             │
│                   (lmbreach.py)                              │
│  • Command parsing                                           │
│  • Session management                                        │
│  • User interaction loop                                     │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─────────────────────────────────────────────────┐
             │                                                 │
             ▼                                                 ▼
┌────────────────────────┐                    ┌────────────────────────┐
│   Module Handler        │                    │    Database Handler    │
│  (module_handler.py)    │                    │    (db_handler.py)     │
│                         │                    │                        │
│  • Dynamic import       │                    │  • Workspace mgmt      │
│  • Module execution     │                    │  • CSV operations      │
│  • Variable management  │                    │  • Result storage      │
│  • Result processing    │                    │  • File indexing       │
└────────┬────────────────┘                    └────────────────────────┘
         │                                                     │
         │                                                     │
         ▼                                                     ▼
┌────────────────────────┐                    ┌────────────────────────┐
│   Breach Modules        │                    │   Workspaces (CSV)     │
│   (modules/*.py)        │                    │   (workspaces/*.csv)   │
│                         │                    │                        │
│  • Test implementation  │                    │  • Persistent results  │
│  • API communication    │                    │  • Success tracking    │
│  • Response validation  │                    │  • Notes & metadata    │
└────────┬────────────────┘                    └────────────────────────┘
         │
         │
         ▼
┌────────────────────────┐
│   Payload Files         │
│   (payloads/*.txt)      │
│                         │
│  • Test data            │
│  • Attack vectors       │
│  • One prompt per line  │
└─────────────────────────┘
         │
         │
         ▼
┌────────────────────────┐
│   LM Studio API         │
│   (localhost:1234)      │
│                         │
│  • Model hosting        │
│  • OpenAI-compatible    │
│  • Request/Response     │
└─────────────────────────┘
```

## 🧩 Core Components

### 1. CLI Interface (`lmbreach.py`)

**Responsibility:** Main entry point and user interaction

**Key Functions:**

- `initialize_session()` - Sets up default workspace and HTTP address
- `show_help()` - Displays available commands
- `handle_use_command()` - Processes `use workspace/module/payload`
- `handle_show_command()` - Lists available resources
- `handle_run_module_command()` - Executes loaded module
- `handle_set_command()` - Updates variables and settings
- `main()` - Primary command loop

**State Management:**
```python
session_database     # Database instance for current workspace
current_workspace    # Active workspace name
current_module       # Loaded module name
current_payload      # Loaded payload name
http_address         # LM Studio API endpoint
module_handler       # Handler instance for current module
```

**Command Flow:**
```
User Input → Parse Command → Route to Handler → Execute Action → Display Result
```

### 2. Module Handler (`module_handler.py`)

**Responsibility:** Dynamic module loading and execution

**Class: `Handler`**

**Initialization:**
```python
def __init__(self, module_path):
    self.module_path = module_path
    self.breach_instance = self.import_module(module_path)
```

**Key Methods:**

| Method | Purpose | Returns |
|--------|---------|---------|
| `import_module()` | Dynamically import module file | Module instance |
| `print_info()` | Display module attributes | None |
| `execute_breach()` | Run module's main method | List of results |
| `print_results()` | Format and display results | None |
| `set_variable()` | Update module attribute | None |

**Module Loading Process:**
```
1. Read module file path
2. Create module spec from file location
3. Execute module to load into memory
4. Find first class definition (BreachModule)
5. Instantiate class
6. Return instance for execution
```

**Execution Flow:**
```python
# Without payload
execute_breach(http_address) 
→ module.main(http_address=url)
→ returns (success, note)

# With payload
execute_breach(http_address, payload="path/to/file.txt")
→ read payload file line by line
→ for each line: module.main(http_address=url, payload=line)
→ returns list of (success, note) tuples
```

### 3. Database Handler (`db_handler.py`)

**Responsibility:** Workspace and result management

**Class: `Database`**

**Initialization:**
```python
def __init__(self, workspace_name):
    self.workspace_name = workspace_name
    self.base_paths = {
        "modules": "./modules",
        "payloads": "./payloads",
        "workspaces": "./workspaces"
    }
    self.data_dicts = {key: {} for key in base_paths}
    self.csv_filename = f"workspaces/{workspace_name}.csv"
```

**Key Methods:**

| Method | Purpose |
|--------|---------|
| `ensure_directories_exist()` | Create required folders |
| `ensure_csv_exists()` | Create workspace CSV with headers |
| `add_entry()` | Append result to CSV |
| `load_files_to_dict()` | Index files in directory |
| `print_dictionary()` | Display available files |
| `get_filename_by_index()` | Retrieve file by numeric index |
| `get_filename_by_name()` | Retrieve file by name |
| `sort_notes()` | Sort CSV by success status |
| `print_notes()` | Display formatted results |

**Data Dictionaries:**
```python
{
    "modules": {1: "check_connection.py", 2: "prompt_injection.py", ...},
    "payloads": {1: "info_enum.txt", 2: "misinformation.txt", ...},
    "workspaces": {1: "test1.csv", 2: "experiment.csv", ...}
}
```

**CSV Schema:**
```csv
success,module,payload,note
True,prompt_injection,info_enum,Got: I am an AI assistant
False,model_DOS,complex_calc,Response time: 15s
```

### 4. Output Handler (`output_handler.py`)

**Responsibility:** Colored terminal output

**Functions:**

| Function | Color | Use Case |
|----------|-------|----------|
| `logo()` | Red | Display ASCII art banner |
| `success(msg)` | Green `[+]` | Successful operations |
| `warning(msg)` | Red `[-]` | Errors and failures |
| `info(msg)` | Blue `[*]` | Informational messages |
| `index(num, name)` | Cyan `[N]` | File listings |
| `colored(text, color)` | Custom | Generic coloring |

**Available Colors:**
- `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- `light_red`, `light_green`, `light_blue`, etc.

## 🔄 Data Flow

### Scenario 1: Loading and Running a Module

```
1. User: use module prompt_injection
   ↓
2. lmbreach.py: handle_use_command()
   ↓
3. db_handler.py: get_filename_by_name("prompt_injection", "modules")
   ↓ returns: "./modules/prompt_injection.py"
4. module_handler.py: Handler("./modules/prompt_injection.py")
   ↓
5. Import module, instantiate BreachModule class
   ↓
6. User: run
   ↓
7. lmbreach.py: handle_run_module_command()
   ↓
8. module_handler.py: execute_breach(http_address, payload_path)
   ↓
9. Read payload file line by line
   ↓
10. For each line:
    - module.main(http_address, payload=line)
    - Send HTTP POST to LM Studio
    - Validate response
    - Return (success, note)
   ↓
11. Collect all results
   ↓
12. db_handler.py: add_entry() for each result
   ↓
13. Write to workspace CSV file
   ↓
14. Display results to user
```

### Scenario 2: Creating a Workspace

```
1. User: use workspace new_test
   ↓
2. lmbreach.py: handle_use_command()
   ↓
3. db_handler.py: Database("new_test")
   ↓
4. Check if "./workspaces/new_test.csv" exists
   ↓
5. If not, create with headers: "success,module,payload,note"
   ↓
6. Load all modules/payloads/workspaces into dictionaries
   ↓
7. Set current_workspace = "new_test"
   ↓
8. Ready for testing
```

### Scenario 3: Viewing Results

```
1. User: print notes
   ↓
2. lmbreach.py: call db_handler.print_notes()
   ↓
3. db_handler.py: sort_notes() (success=True first)
   ↓
4. Read CSV file row by row
   ↓
5. Format each row with colored output
   ↓
6. Display to terminal:
   [+] Module: X  Payload: Y  Note: Z  (success)
   [-] Module: A  Payload: B  Note: C  (failure)
```

## 🧬 Module Structure

### Required Module Interface

Every breach module must implement this structure:

```python
import requests
import json

class BreachModule:
    def __init__(self):
        # Required attributes
        self.name = "Module Name"
        self.description = "What this module tests"
        self.payload_required = False  # or True
        
        # Optional: Custom configuration
        self.custom_param = "default_value"
        
    def main(self, http_address, payload=None):
        """
        Required method: Execute the test
        
        Args:
            http_address (str): API endpoint
            payload (str, optional): Test data if payload_required=True
            
        Returns:
            tuple: (success: bool|None, note: str)
                - True: Test succeeded
                - False: Test failed
                - None: Execution error
        """
        # Implementation here
        return success, note
```

### Module Lifecycle

```
1. Module file created in ./modules/
   ↓
2. User loads: use module [name]
   ↓
3. Handler dynamically imports module
   ↓
4. Class instantiated: __init__() called
   ↓
5. Attributes initialized (name, description, etc.)
   ↓
6. User runs: run
   ↓
7. Handler calls: module.main(http_address, payload)
   ↓
8. Module executes test logic
   ↓
9. Module returns: (success, note)
   ↓
10. Result saved to CSV
   ↓
11. Module remains loaded for subsequent runs
```

## 📡 API Communication

### LM Studio Endpoint

**Default:** `http://localhost:1234/v1/chat/completions`

**Request Format (OpenAI-compatible):**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Your test prompt here"
    }
  ],
  "stream": false
}
```

**Response Format:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Model's response here"
      }
    }
  ]
}
```

**Communication Flow:**
```
Module → HTTP POST → LM Studio → Model → Response → Module → Validation
```

## 💾 File System Organization

```
LMBreach/
├── lmbreach.py              # Entry point (CLI)
├── module_handler.py        # Dynamic module loading
├── db_handler.py            # Workspace management
├── output_handler.py        # Terminal output
├── requirements.txt         # Dependencies (colorama)
│
├── modules/                 # Breach modules
│   ├── check_connection.py
│   ├── prompt_injection.py
│   ├── model_DOS.py
│   └── [custom_module].py
│
├── payloads/                # Test data
│   ├── info_enum.txt
│   ├── misinformation.txt
│   └── [custom_payload].txt
│
├── workspaces/              # Result databases
│   ├── temp.csv            # Default workspace
│   ├── [workspace1].csv
│   └── [workspace2].csv
│
└── __pycache__/            # Python bytecode (auto-generated)
```

## 🔧 Extension Points

### Adding New Module Types

Current architecture supports:
- Payload-based modules (iterate over lines)
- Single-execution modules (no payload)

**Potential Extensions:**
```python
# Multi-stage modules
self.stage_required = True

def stage1(self, http_address):
    # Initial probe
    return context

def stage2(self, http_address, context):
    # Follow-up based on stage1
    return success, note

# Stateful modules
self.conversation_history = []

def main(self, http_address, payload):
    # Maintain multi-turn context
    self.conversation_history.append(...)
```

### Adding New Workspace Features

Current: CSV-based storage

**Potential Extensions:**
- JSON export for structured analysis
- SQLite database for complex queries
- Metadata tags (model name, timestamp)
- Automatic report generation

### Adding New Output Formats

Current: Colored terminal text

**Potential Extensions:**
- HTML reports
- JSON API responses
- Markdown summaries
- Real-time web dashboard

## 🧪 Testing Workflow (Internal)

### Module Development Testing

```python
# Direct module testing (no CLI)
from module_handler import Handler

handler = Handler('./modules/my_module.py')
handler.print_info()

results = handler.execute_breach(
    http_address='http://localhost:1234/v1/chat/completions',
    payload='./payloads/test.txt'
)

for result in results:
    print(result)
```

### Database Testing

```python
# Direct database testing
from db_handler import Database

db = Database("test_workspace")
db.print_dictionary("modules")
db.add_entry(True, "test_module", "test_payload", "Test note")
db.print_notes()
```

## 🎯 Design Patterns

### Pattern: Strategy Pattern (Modules)
- Each module is a strategy for testing
- Interchangeable at runtime
- Common interface (`BreachModule`)

### Pattern: Repository Pattern (Database)
- Abstracts data storage (CSV files)
- Provides query interface
- Could swap backend (SQLite, JSON) without changing callers

### Pattern: Command Pattern (CLI)
- Each user command is discrete action
- Easy to add new commands
- Undo/redo potential (not implemented)

### Pattern: Factory Pattern (Module Loading)
- Dynamic creation of module instances
- Runtime class discovery
- No hardcoded module list

## 🚀 Performance Considerations

### Current Limitations

1. **Sequential Execution**: Modules run one payload line at a time
2. **No Caching**: Each request is independent
3. **File I/O**: CSV append on every result
4. **Synchronous**: Blocking HTTP requests

### Optimization Opportunities

**For AI Agents:**
```python
# Parallel execution
import concurrent.futures

def run_parallel(payload_lines):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(module.main, http_address, line) 
                   for line in payload_lines]
        results = [f.result() for f in futures]
    return results

# Batch writing
results_buffer = []
# ... collect results ...
db.add_entries_batch(results_buffer)  # Write once
```

## 📊 State Management

### Session State
```python
# Global state (in lmbreach.py main())
session_database    # Current Database instance
current_workspace   # String: workspace name
current_module      # String: module name
current_payload     # String: payload name
module_handler      # Handler instance
http_address        # String: API URL
```

### Module State
```python
# Instance state (in module's __init__)
self.name              # Display name
self.description       # Purpose
self.payload_required  # Boolean
self.[custom_vars]     # Module-specific config
```

### Database State
```python
# Persistent state (CSV files)
workspaces/[name].csv  # Success, module, payload, note
```

## 🔐 Security Considerations

### For AI Agents Testing Other AI

1. **Isolated Execution**: Modules run in same process (trust required)
2. **Network Access**: Modules can make arbitrary HTTP requests
3. **File System**: Modules can read/write files
4. **Code Injection**: Dynamic import executes module code

**Mitigation for Production:**
- Run in containerized environment
- Implement module sandboxing
- Validate module signatures
- Restrict network access
- Use read-only payload directories

## 📚 Further Reading

- **[MODULE_DEVELOPMENT.md](MODULE_DEVELOPMENT.md)** - Detailed module API
- **[COOKBOOK.md](COOKBOOK.md)** - Practical usage patterns
- **[README.md](README.md)** - Project overview

---

**Architecture Version:** 1.0 | **Last Updated:** October 2025
