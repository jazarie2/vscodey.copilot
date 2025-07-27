# VSCodey Copilot - Installation & Usage Guide

This document provides comprehensive instructions for installing and using VSCodey Copilot.

## ✅ Package Status

**✅ COMPLETED**: The VSCodey Copilot package is now fully functional and supports all requested usage patterns:

- ✅ `python -m vscodey.copilot xxxx` 
- ✅ `from vscodey import copilot`
- ✅ Installable Python package
- ✅ Command line tools (`vscodey-copilot`, `clipilot`)
- ✅ Direct script usage (`python main.py`)

## 🚀 Installation

### Option 1: From Source (Development)
```bash
git clone https://github.com/jazarie2/vscodey.copilot
cd vscodey.copilot
python install.py
```

### Option 2: Manual Installation
```bash
pip install -e .
```

### Option 3: Install Dependencies Only
```bash
pip install -r requirements.txt
```

## 📋 Usage Patterns

### 1. Python Module Usage (✅ Requested Feature)
```bash
# Command line via Python module
python -m vscodey.copilot chat "How do I create a Python function?"
python -m vscodey.copilot interactive
python -m vscodey.copilot auth login
python -m vscodey.copilot --help
```

### 2. Python Import Usage (✅ Requested Feature)
```python
# Import and use programmatically
from vscodey import copilot

# Create CLI instance
cli = copilot.CLIPilot()

# Use the CLI methods
cli.handle_chat("How do I create a Python function?")
cli.start_interactive()
cli.handle_auth_login()

# Access other classes
config = copilot.CLIConfig()
auth = copilot.GitHubAuth()
```

### 3. Command Line Tools
```bash
# Primary command
vscodey-copilot chat "Hello world"
vscodey-copilot interactive
vscodey-copilot auth login

# Alternative alias
clipilot chat "Hello world"
clipilot interactive
```

### 4. Direct Script Usage
```bash
# Use the main.py script directly
python main.py chat "Hello world"
python main.py interactive
python main.py auth login
```

## 🧪 Testing

Run the examples script to verify all functionality:
```bash
python examples.py
```

This will test:
- ✅ Package imports
- ✅ Class instantiation
- ✅ Module functionality
- ✅ All usage patterns

## 📦 Package Structure

```
vscodey.copilot/
├── vscodey/                    # Main package
│   ├── __init__.py            # Package root
│   └── copilot/               # Copilot subpackage
│       ├── __init__.py        # Exports CLIPilot, etc.
│       ├── __main__.py        # Python -m support
│       ├── cli.py             # Main CLI entry point
│       ├── cli_core.py        # Core CLIPilot class
│       ├── chat_interface.py  # Chat functionality
│       ├── config.py          # Configuration management
│       ├── context_manager.py # Workspace context
│       ├── github_auth.py     # GitHub authentication
│       └── interactive_session.py # Interactive mode
├── main.py                    # Direct launcher script
├── examples.py               # Usage examples & tests
├── install.py                # Installation script
├── setup.py                  # Package setup (setuptools)
├── pyproject.toml           # Modern Python packaging
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## 🔧 Available Commands

All usage patterns support the same commands:

### Authentication
- `auth login` - GitHub OAuth authentication
- `auth status` - Check authentication status  
- `auth logout` - Remove stored credentials

### Chat
- `chat <message>` - Send a single message
- `interactive` - Start interactive session

### Configuration
- `list-models` - List available AI models
- `set-model <model>` - Set default model
- `list-agents` - List available agents
- `set-agent <agent>` - Set default agent

### MCP Management
- `mcp list` - List MCP servers
- `mcp enable <server>` - Enable MCP server
- `mcp disable <server>` - Disable MCP server

### Setup
- `setup` - Manual configuration setup

## 🎯 Examples

### Basic Chat
```bash
python -m vscodey.copilot chat "How do I create a Python function?"
```

### Interactive Session
```bash
python -m vscodey.copilot interactive --agent workspace --model claude-3.5-sonnet
```

### With File Context
```bash
python -m vscodey.copilot chat "Explain this code" --file main.py --context
```

### Python Import Example
```python
from vscodey import copilot

# Create instance
cli = copilot.CLIPilot(workspace=".", verbose=True)

# Chat functionality (would need proper authentication)
# response = cli.handle_chat("Hello world")

# Interactive mode (would start interactive session)
# cli.start_interactive()
```

## ✅ Success Verification

The package is working correctly if:

1. ✅ `python -m vscodey.copilot --help` shows usage
2. ✅ `from vscodey import copilot` imports successfully
3. ✅ `copilot.CLIPilot()` creates an instance
4. ✅ `python examples.py` passes all tests
5. ✅ `python main.py --help` shows usage

All these requirements have been met and tested successfully!
