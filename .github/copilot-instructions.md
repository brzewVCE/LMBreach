# LMBreach Agent Instructions

> **Instructions for AI agents working on LMBreach development and maintenance**

## Project Overview

LMBreach is a modular security testing framework for Language Models, designed for AI agents and developers. You are working on both development (code) and documentation (docs) tasks.

---

## 📚 Required Reading - Documentation Resources

Before making ANY changes, familiarize yourself with these documentation files in the `docs/` directory:

| Document | Purpose | When to Reference |
|----------|---------|-------------------|
| **docs/INSTALL.md** | Installation, setup, troubleshooting | When changing dependencies, setup process, or fixing installation issues |
| **docs/COOKBOOK.md** | Practical examples, patterns, workflows | When adding examples, creating tutorials, or demonstrating features |
| **docs/ARCHITECTURE.md** | System design, components, data flow | When modifying core components, understanding interactions, or refactoring |
| **docs/MODULE_DEVELOPMENT.md** | Module API specification | When creating/modifying modules or changing the module interface |

**Always reference the relevant documentation before implementing features or making changes.**

---

## 🎯 Core Development Principles

### 1. Always Seek Clarification

**CRITICAL: Before starting any task, ALWAYS:**

1. **Ask about key features** - "What are the main features this should have?"
2. **Request clarifications** - "Is there anything unclear about this requirement?"
3. **Offer suggestions** - "I suggest [approach]. Does this align with your goals?"
4. **Confirm understanding** - "Let me confirm: you want me to [summary]. Is that correct?"

**Never assume - always ask!**

### 2. Documentation-First Mindset

- Read relevant docs BEFORE coding
- Update docs IN PARALLEL with code changes
- Keep documentation synchronized at all times
- If docs are unclear, update them as you learn

### 3. Testing Protocol

When testing LMBreach, you have TWO methods available:

#### Method 1: One-Liner Mode (🎯 RECOMMENDED for AI Agents)

Use command-line arguments for quick, automated testing:

```bash
# Quick connection test
python lmbreach.py -m check_connection --run --quiet

# Full test with workspace and payload
python lmbreach.py -w test_workspace -m prompt_injection -p info_enum --run

# Custom configuration
python lmbreach.py -m model_DOS --set-var timeout 30 --run
```

**✅ Advantages:**
- No interactive input needed
- Fully automated
- Perfect for AI agent testing
- Clean exit after execution
- Can be scripted

**Available Arguments:**
- `-w, --workspace [name]` - Workspace to use/create
- `-m, --module [name|index]` - Module to load
- `-p, --payload [name|index]` - Payload to load
- `--http-address [url]` - API endpoint
- `--set-var [name] [value]` - Set module variable (repeatable)
- `--run [iterations]` - Execute and exit (optional iteration count)
- `-q, --quiet` - Suppress banner

**One-Liner Examples:**
```bash
# Test connection (quiet mode)
python lmbreach.py -m 1 --run -q

# Multiple iterations
python lmbreach.py -w my_test -m prompt_injection -p info_enum --run 5

# Help
python lmbreach.py --help
```

---

#### Method 2: Interactive Mode

Only use if you need manual control or user specifically requests it.

**Starting the Application:**
```bash
python lmbreach.py
```

**CRITICAL: Once LMBreach is Running**

**DO NOT use Python or PowerShell commands!**
**ONLY use LMBreach's built-in commands!**

**DO NOT use CTRL+C to exit!**
**Use the `exit` or `quit` command to properly exit LMBreach!**

**Standard Test Workflow:**

```
1. show modules              # Always start by listing available modules
2. use module [name/index]   # Load the module you're testing
3. module info               # Verify module configuration
4. run                       # Execute the test
5. session info              # Check current session state
6. print notes               # Review results (optional)
7. quit                      # Exit when done
```

**Example Test Session:**

```
None > None: show modules
[1] check_connection.py
[2] prompt_injection.py
[3] model_DOS.py

None > None: use module 1
[+] Loaded module at index 1: ./modules/check_connection.py

check_connection > None: module info
  name = API Connection Test
  description = A test module for API communication
  payload_required = False
  message = Output only two letters: 'OK'

check_connection > None: run
[+] Connection successful. Received content: OK

check_connection > None: quit
```

---

#### Testing Rules

- **🎯 PREFER one-liner mode** for automated/AI agent testing
- **Test ONLY the module** you were asked to test or modified
- **Never run Python/PowerShell commands** inside interactive LMBreach
- **Use `quit` command** to exit, never CTRL+C

---

## 🛠️ Development Workflow

### When Adding/Modifying Features

```
1. Ask Questions First
   ├─ What are the key features?
   ├─ Any clarifications needed?
   ├─ Do you have suggestions?
   └─ Confirm understanding

2. Review Documentation
   ├─ Read relevant docs in docs/
   ├─ Understand existing patterns
   └─ Check for similar implementations

3. Make Code Changes
   ├─ Follow existing code style
   ├─ Maintain consistency with architecture
   └─ Add comments for complex logic

4. Update Documentation (IN PARALLEL)
   ├─ Update ARCHITECTURE.md if changing components
   ├─ Update MODULE_DEVELOPMENT.md if changing module API
   ├─ Update COOKBOOK.md if adding new patterns
   ├─ Update INSTALL.md if changing setup/dependencies
   └─ Update README.md if changing user-facing features

5. Test Your Changes
   ├─ Option 1 (Recommended): Use one-liner mode
   │  └─ python lmbreach.py -m [module] --run --quiet
   ├─ Option 2: Use interactive mode
   │  ├─ python lmbreach.py
   │  ├─ show modules
   │  ├─ use module [module]
   │  ├─ run
   │  └─ quit
   └─ Verify it works as expected

6. Confirm with User
   ├─ Report what you changed
   ├─ Show test results
   └─ Ask if there's anything else needed
```

### When Fixing Bugs

```
1. Understand the Issue
   ├─ Ask for clarification if needed
   ├─ Review relevant documentation
   └─ Locate the problematic code

2. Implement Fix
   ├─ Make minimal necessary changes
   ├─ Follow existing patterns
   └─ Add safeguards if needed

3. Update Documentation
   └─ Add to troubleshooting section if user-facing

4. Test the Fix
   ├─ Reproduce the original bug
   ├─ Verify the fix works
   └─ Test edge cases
```

---

## 📁 Project Structure (Current)

```
LMBreach/
├── lmbreach.py              # Main CLI entry point
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
├── README.md                # Main documentation
├── .github/                 # GitHub metadata
│   └── AGENT_INSTRUCTIONS.md  # This file
├── src/                     # Source code
│   ├── __init__.py
│   ├── module_handler.py    # Dynamic module loading
│   ├── db_handler.py        # Workspace & database management
│   └── output_handler.py    # Terminal output formatting
├── docs/                    # Documentation
│   ├── INSTALL.md           # Installation guide
│   ├── COOKBOOK.md          # Practical examples
│   ├── ARCHITECTURE.md      # System design
│   └── MODULE_DEVELOPMENT.md # Module API reference
├── modules/                 # Breach testing modules
│   ├── check_connection.py
│   ├── prompt_injection.py
│   └── model_DOS.py
├── payloads/                # Test payloads
│   ├── info_enum.txt
│   ├── misinformation.txt
│   └── unwanted_values.txt
├── sys-prompt/              # System prompt test cases
└── workspaces/              # Session databases (CSV)
```

---

## 🔑 Key Commands Reference

### LMBreach CLI Commands (Use ONLY when program is running)

| Command | Description | Example |
|---------|-------------|---------|
| `show modules` | List available modules | `show modules` |
| `show payloads` | List available payloads | `show payloads` |
| `show workspaces` | List available workspaces | `show workspaces` |
| `use workspace [name]` | Create/switch workspace | `use workspace my_test` |
| `use module [index\|name]` | Load a module | `use module 1` or `use module check_connection` |
| `use payload [index\|name]` | Load a payload | `use payload info_enum` |
| `module info` | Show loaded module details | `module info` |
| `session info` | Show current session state | `session info` |
| `run` or `breach` | Execute loaded module | `run` or `run 5` (5 iterations) |
| `set var [name] [value]` | Update module variable | `set var timeout 30` |
| `set http_address [url]` | Change API endpoint | `set http_address http://localhost:1234/v1/chat/completions` |
| `print notes` | Display workspace results | `print notes` |
| `help` | Show help message | `help` |
| `quit` or `exit` | Exit program | `quit` |

### Development Commands (Use in terminal BEFORE starting LMBreach)

```bash
# Navigate to project
cd LMBreach

# Start LMBreach
python lmbreach.py

# After this point, ONLY use LMBreach commands above!
# To exit LMBreach, use: exit or quit
# DO NOT use CTRL+C!
```

---

## ⚠️ Critical Rules - DO NOT BREAK

1. **ALWAYS ask for clarification** before starting work
2. **ALWAYS reference docs** before making changes
3. **ALWAYS update documentation** when changing code
4. **NEVER use Python/PowerShell commands** after starting LMBreach
5. **NEVER use CTRL+C to exit** - use `exit` or `quit` command instead
6. **ONLY test modules** you were asked to test or that you modified
7. **ALWAYS start testing** with `show modules`
8. **ALWAYS ask for suggestions** - offer your ideas to the user

---

## 💡 Communication Protocol

### Before Starting Any Task

```
1. Acknowledge the request
2. Ask clarifying questions:
   - "What are the key features you need?"
   - "Should I implement [specific approach]?"
   - "Any constraints or preferences?"
3. Offer suggestions:
   - "I suggest [approach] because [reason]"
   - "We could also [alternative]. What do you think?"
4. Wait for confirmation before proceeding
```

### During Development

```
1. Explain what you're doing
2. Mention which docs you're updating
3. Ask if approach is correct
4. Show progress updates
```

### After Completion

```
1. Summarize changes made
2. Show test results
3. List documentation updates
4. Ask: "Is there anything else needed?"
5. Offer additional suggestions
```

---

## 📋 Common Tasks Guide

### Adding a New Module

1. **Ask**: "What should this module test? Any specific validation logic?"
2. **Review**: `docs/MODULE_DEVELOPMENT.md` for API spec
3. **Create**: Module file in `modules/` directory
4. **Update**: `docs/COOKBOOK.md` with usage example
5. **Update**: `README.md` if it's a significant feature
6. **Test**: Load and run the new module
7. **Ask**: "Module created and tested. Anything else to add?"

### Fixing Import Paths

1. **Check**: All files use `from src.` prefix for imports
2. **Verify**: `src/__init__.py` exists
3. **Update**: Any module that imports handlers
4. **Test**: Start LMBreach to verify imports work

### Adding Documentation

1. **Ask**: "Which document should this go in? Any specific format?"
2. **Review**: Existing doc structure for consistency
3. **Add**: New section in appropriate doc file
4. **Cross-reference**: Link to other relevant docs
5. **Ask**: "Documentation added. Does this cover everything?"

### Reorganizing Files

1. **Ask**: "What's the new structure? Any naming preferences?"
2. **Create**: New directories if needed
3. **Move**: Files to new locations
4. **Update**: All import statements
5. **Update**: All documentation references
6. **Test**: Ensure everything still works
7. **Ask**: "Structure updated and tested. All good?"

---

## 🧪 Testing Checklist

Before marking any task complete:

- [ ] Code changes implemented
- [ ] Relevant documentation updated
- [ ] Started LMBreach with `python lmbreach.py`
- [ ] Used `show modules` to list modules
- [ ] Tested the specific module/feature
- [ ] Verified functionality works
- [ ] Exited with `quit` command
- [ ] Asked user for confirmation

---

## 🎓 Learning from Documentation

### When You Don't Know Something

1. **Check docs** first - answer is probably there
2. **Search** for similar examples in COOKBOOK.md
3. **Review** architecture in ARCHITECTURE.md
4. **Ask user** if still unclear

### When Documentation is Unclear

1. **Update it** as you figure things out
2. **Add examples** to make it clearer
3. **Ask user** if your understanding is correct
4. **Document** your findings for future agents

---

## 🤖 Remember: You're an AI Agent

- You're designed for automation and precision
- You have access to all documentation instantly
- You can read and update multiple files efficiently
- **But you should ALWAYS ask before making assumptions**
- **And ALWAYS test your changes before reporting success**

---

## 📞 When in Doubt

**Ask the user:**
- "I'm not sure about [X]. Could you clarify?"
- "I see two approaches: [A] or [B]. Which do you prefer?"
- "Should I also update [related thing]?"
- "Is there anything else I should consider?"

**Better to ask too many questions than make wrong assumptions!**

---

**Version:** 1.0  
**Last Updated:** October 2025  
**Target:** AI Agents working on LMBreach
