# Installation Guide

This guide will walk you through setting up LMBreach on your system.

## 📋 Prerequisites

### Required Software

1. **Python 3.11+**
   - LMBreach is developed and tested with Python 3.11
   - Earlier versions may work but are not officially supported
   - Check your version: `python --version`

2. **LM Studio**
   - Download from: [https://lmstudio.ai/](https://lmstudio.ai/)
   - LM Studio provides a local API server for running language models
   - Supports various model formats (GGUF, etc.)

3. **Git** (for cloning the repository)
   - Download from: [https://git-scm.com/](https://git-scm.com/)

### System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: Depends on the LLM you plan to test (minimum 8GB recommended)
- **Disk Space**: ~100MB for LMBreach + space for LM Studio and models

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/brzewVCE/LMBreach.git

# Navigate into the directory
cd LMBreach
```

**Alternative: Download ZIP**
- Go to the GitHub repository
- Click "Code" → "Download ZIP"
- Extract to your desired location
- Open terminal in that directory

### Step 2: Install Python Dependencies

LMBreach has minimal dependencies for maximum compatibility:

```bash
# Install required packages
pip install -r requirements.txt
```

**Current dependencies:**
- `colorama` - Cross-platform colored terminal output

**For virtual environment (recommended):**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Set Up LM Studio

1. **Install LM Studio**
   - Download and install from [lmstudio.ai](https://lmstudio.ai/)
   - Launch the application

2. **Download a Model**
   - In LM Studio, click "Search" or "Discover"
   - Download a model (e.g., `llama-2-7b`, `mistral-7b`, `phi-3`)
   - Smaller models (7B parameters) work well for testing

3. **Start the Local Server**
   - In LM Studio, click "Local Server" tab
   - Click "Start Server"
   - Default address: `http://localhost:1234`
   - **Important**: Keep this server running while using LMBreach

4. **Verify Server is Running**
   - Check that LM Studio shows "Server Running"
   - Note the port (default: 1234)

### Step 4: Verify Installation

```bash
# Launch LMBreach
python lmbreach.py
```

You should see:
```
 _    ___  ________                     _     
| |   |  \/  | ___ \                   | |    
| |   | .  . | |_/ /_ __ ___  __ _  ___| |__  
| |   | |\/| | ___ \ '__/ _ \/ _` |/ __| '_ \ 
| |___| |  | | |_/ / | |  __/ (_| | (__| | | |
\_____|_|  |_|____/|_|  \___|\__,_|\___|_| |_|

None > None:
```

**Test the connection:**

```bash
# In LMBreach prompt
use module 1
run
```

If successful, you'll see:
```
[+] Connection successful. Received content: OK
```

## 🔍 Verification Checklist

- [ ] Python 3.11+ installed and accessible
- [ ] LMBreach repository cloned/downloaded
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] LM Studio installed and a model downloaded
- [ ] LM Studio server running on `http://localhost:1234`
- [ ] LMBreach launches without errors
- [ ] Connection test module executes successfully

## 🐛 Troubleshooting

### Issue: "Module not found" or Import Errors

**Solution:**
```bash
# Ensure you're in the LMBreach directory
cd LMBreach

# Verify requirements are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

### Issue: "Connection Failed" When Running Modules

**Possible Causes:**

1. **LM Studio server is not running**
   - Open LM Studio → Local Server → Start Server

2. **Wrong port or address**
   ```bash
   # Check LM Studio's server address
   # In LMBreach, update if needed:
   set http_address http://localhost:1234/v1/chat/completions
   ```

3. **No model loaded in LM Studio**
   - Load a model in LM Studio before starting the server

4. **Firewall blocking localhost**
   - Allow Python and LM Studio through your firewall

### Issue: "No module named 'colorama'"

**Solution:**
```bash
# Install colorama directly
pip install colorama

# Or reinstall all requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: LMBreach Launches but Commands Don't Work

**Solution:**
- Check for typos in commands
- Use `help` command to see available commands
- Ensure you're using lowercase for commands
- Example: `use module 1` not `USE MODULE 1`

### Issue: "Permission Denied" When Creating Workspaces

**Solution:**
```bash
# Ensure you have write permissions in the directory
# On Linux/Mac:
chmod -R u+w LMBreach

# Run from a directory where you have write access
```

### Issue: Slow Response Times or Timeouts

**Possible Causes:**
- Model is too large for your hardware
- LM Studio settings (context length, batch size)

**Solution:**
- Try a smaller model (7B instead of 13B)
- Adjust LM Studio performance settings
- Increase timeout in DoS module: `set var timeout 60`

## 🔄 Updating LMBreach

```bash
# Navigate to LMBreach directory
cd LMBreach

# Pull latest changes
git pull origin main

# Update dependencies (if requirements changed)
pip install -r requirements.txt --upgrade
```

## 🧪 Testing Your Installation

Create a simple test workflow:

```bash
# Start LMBreach
python lmbreach.py

# Create a test workspace
use workspace installation_test

# Load connection module
use module check_connection

# Check module configuration
module info

# Run the test
run

# View results
print notes

# Clean up (optional)
quit
```

**Expected Output:**
- Module loads successfully
- Connection test returns "OK"
- Results saved to workspace CSV

## 📦 Optional: Development Setup

For contributors or advanced users:

```bash
# Install development dependencies (if any)
pip install -r requirements.txt

# Run in development mode
python lmbreach.py

# Create custom modules
# See MODULE_DEVELOPMENT.md for details
```

## 🎯 Next Steps

Once installation is verified:

1. **Read the [Cookbook](COOKBOOK.md)** for practical examples
2. **Explore [Architecture](ARCHITECTURE.md)** to understand the system
3. **Check [Module Development](MODULE_DEVELOPMENT.md)** to create custom tests
4. **Start testing** with the built-in modules

## 💡 Tips for AI Agents

If you're an AI agent setting up LMBreach:

- All Python dependencies are minimal and standard
- The tool is designed for CLI automation
- File paths are absolute, making programmatic control easier
- CSV output format is machine-readable
- Module results return structured success/failure data

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check existing GitHub Issues
2. Review the [Architecture](ARCHITECTURE.md) documentation
3. Examine module source code for examples
4. Create a new GitHub Issue with:
   - Your OS and Python version
   - LM Studio version
   - Error messages (full traceback)
   - Steps to reproduce

---

**Installation complete!** You're ready to start testing language models with LMBreach.
