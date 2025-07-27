# VSCodey Copilot - GitHub Copilot Chat for Command Line

**VSCodey Copilot** brings GitHub Copilot Chat functionality to your command line interface, allowing you to interact with AI-powered coding assistance directly from your terminal without needing VS Code.

## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install vscodey-copilot
```

### From Source
```bash
git clone https://github.com/jazarie2/vscodey.copilot
cd vscodey.copilot
pip install -e .
```

## 🚀 Quick Start

### Command Line Usage
```bash
# Setup: Configure with your credentials
vscodey-copilot setup

# Single chat: Ask a quick question
vscodey-copilot chat "How do I create a Python function?"

# Interactive mode: Start a persistent chat session
vscodey-copilot interactive

# Alternative command alias
clipilot chat "Hello, help me get started!"
```

### Python Module Usage
```bash
# Use as a Python module
python -m vscodey.copilot chat "Explain this code"
python -m vscodey.copilot interactive
```

### Python Import Usage
```python
from vscodey import copilot

# Create CLI instance
cli = copilot.CLIPilot()

# Single chat
response = cli.handle_chat("How do I create a Python function?")

# Interactive session
cli.start_interactive()
```

## 🚀 Features

- **🤖 4 Specialized AI Agents**: Workspace, VS Code, Terminal, and Agent Mode
- **🧠 7 AI Models**: GPT-4.1, GPT-4o Mini, Claude 3.5/3.7 Sonnet, Gemini 2.0 Flash, O1, O1-mini
- **💬 Interactive Chat**: Persistent chat sessions with conversation history
- **🖥️ Real Command Execution**: Terminal agent executes actual shell commands
- **📁 MCP Tool Integration**: Filesystem, web search, and GitHub operations
- **🔧 Workspace Intelligence**: Automatic project analysis and context gathering
- **⚙️ Dynamic Configuration**: Model switching, agent selection, and MCP management
- **🔐 Secure Authentication**: GitHub OAuth and token management

## 🎯 AI Agents

### 🏢 **Workspace Agent** (Default)
Specializes in project-wide operations, file analysis, and code understanding.
```bash
vscodey-copilot chat "analyze the project structure" --agent workspace
```

### 🎨 **VS Code Agent**
Helps with VS Code features, extensions, settings, and editor functionality.
```bash
vscodey-copilot chat "how to configure debugging" --agent vscode
```

### 🖥️ **Terminal Agent**
Executes real shell commands and assists with terminal workflows.
```bash
vscodey-copilot chat "show current directory" --agent terminal
```

### 🤖 **Agent Mode**
Autonomous multi-step task execution with MCP tool integration.
```bash
vscodey-copilot chat "read main.py and analyze its structure" --agent agent
```

## 📋 Command Reference

### Authentication
```bash
vscodey-copilot auth login    # GitHub OAuth authentication
vscodey-copilot auth status   # Check authentication status
vscodey-copilot auth logout   # Remove stored credentials
```

### Chat
```bash
vscodey-copilot chat <message> [OPTIONS]
  --file, -f <path>          # Include specific files
  --context, -c              # Include workspace context
  --agent <agent-id>         # Use specific agent
  --model <model-id>         # Use specific model
  --workspace <path>         # Specify workspace directory
  --verbose                  # Enable verbose output
```

### Interactive Mode
```bash
vscodey-copilot interactive --agent workspace --model claude-3.5-sonnet
```

### Model & Agent Management
```bash
vscodey-copilot list-models             # List all available models
vscodey-copilot set-model <model-id>    # Set default model
vscodey-copilot list-agents             # List all available agents
vscodey-copilot set-agent <agent-id>    # Set default agent
```

### MCP Server Management
```bash
vscodey-copilot mcp list                # List MCP servers
vscodey-copilot mcp enable <server-id>  # Enable MCP server
vscodey-copilot mcp disable <server-id> # Disable MCP server
```

## 🧠 Available AI Models

- **GPT Models**: gpt-4.1-2025-04-14, gpt-4o-mini
- **Claude Models**: claude-3.5-sonnet, claude-3.7-sonnet
- **Gemini Models**: gemini-2.0-flash-001
- **OpenAI O1 Models**: o1, o1-mini (Advanced Reasoning)

## 🔧 MCP (Model Context Protocol) Tools

- **📁 Filesystem MCP Server**: Real file operations and directory navigation
- **🔍 Brave Search MCP Server**: Web search capabilities
- **🐙 GitHub MCP Server**: GitHub repository operations and API access

## 💡 Usage Examples

### 🌐 MCP Browser Research
```bash
# Enable browser search
vscodey-copilot mcp enable brave-search

# Research questions requiring web search
vscodey-copilot chat "What are the latest Python security best practices for 2025?" --agent agent
vscodey-copilot chat "Find current FastAPI performance benchmarks" --agent agent
```

### 📁 Workspace & File Analysis
```bash
# Analyze entire project
vscodey-copilot chat "Analyze this project structure and identify issues" --context --agent workspace

# Review specific files
vscodey-copilot chat "Review this code for bugs and improvements" --file main.py --agent workspace

# Fix issues with context
vscodey-copilot chat "Fix import errors and improve error handling" --file vscodey/copilot/cli.py --context --agent workspace
```

### 🧠 Model Switching for Feature Development
```bash
# Phase 1: Architecture planning (O1 for complex reasoning)
vscodey-copilot set-model o1
vscodey-copilot chat "Design architecture for adding a plugin system" --context --agent workspace

# Phase 2: Implementation (Claude for detailed coding)
vscodey-copilot set-model claude-3.5-sonnet
vscodey-copilot chat "Implement the plugin loader class" --file vscodey/copilot/cli_core.py --agent workspace

# Phase 3: Testing (Gemini for test generation)
vscodey-copilot set-model gemini-2.0-flash-001
vscodey-copilot chat "Generate comprehensive tests for the plugin system" --context --agent workspace
```

### Code Analysis
```bash
vscodey-copilot chat "analyze this project structure" --agent workspace --context
vscodey-copilot chat "explain this code" --file main.py --agent workspace
```

### Terminal Operations
```bash
vscodey-copilot chat "show current directory" --agent terminal
vscodey-copilot chat "find all Python files" --agent terminal
```

### Agent Mode - File Operations
```bash
vscodey-copilot chat "read package.json and tell me about dependencies" --agent agent
vscodey-copilot chat "find all TODO comments in Python files" --agent agent
```

## 🛠️ Development

### 📚 Example Files
The repository includes comprehensive examples:

- **`demo.py`** - Interactive demo with all scenarios
- **`advanced_examples.py`** - Detailed examples with explanations  
- **`examples.py`** - Basic package testing and usage
- **`EXAMPLES.md`** - Quick reference guide

Run the interactive demo:
```bash
python demo.py
```

View all examples:
```bash
python advanced_examples.py
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Running from Source
```bash
git clone https://github.com/jazarie2/vscodey.copilot
cd vscodey.copilot
pip install -e .
vscodey-copilot --help
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/jazarie2/vscodey.copilot/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/jazarie2/vscodey.copilot/discussions)
- 📧 **Contact**: [contact@vscodey.dev](mailto:contact@vscodey.dev)

---

*Happy coding with VSCodey Copilot! 🚀*