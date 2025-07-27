# Quick Reference: VSCodey Copilot Examples

This document provides quick examples for the three key scenarios you requested.

## 1. 🌐 MCP Browser Research Questions

### Enable Browser MCP
```bash
# First, enable the browser MCP server
vscodey-copilot mcp enable brave-search
```

### Research Questions (Command Line)
```bash
# Research latest technologies
vscodey-copilot chat "What are the latest Python security vulnerabilities in 2025?" --agent agent

# Find best practices
vscodey-copilot chat "Find current FastAPI security best practices and examples" --agent agent

# Compare technologies
vscodey-copilot chat "Compare the latest Python web frameworks for performance" --agent agent

# Research documentation
vscodey-copilot chat "Find the best Python async/await tutorials and examples" --agent agent
```

### Python Import Usage
```python
from vscodey import copilot

# Enable browser research
cli = copilot.CLIPilot()
cli.manage_mcp_server("enable", "brave-search")

# Ask research questions
response = cli.handle_chat(
    "What are the latest Python 3.12 security features?",
    agent="agent",
    model="claude-3.5-sonnet"
)
```

## 2. 📁 Workspace/File Analysis to Fix Issues

### Analyze Entire Project
```bash
# Get project overview
vscodey-copilot chat "Analyze this project structure and identify issues" --context --agent workspace

# Security analysis
vscodey-copilot chat "Review this project for security vulnerabilities" --context --agent workspace
```

### Analyze Specific Files
```bash
# Review single file
vscodey-copilot chat "Review this file for bugs and improvements" --file main.py --agent workspace

# Multiple files
vscodey-copilot chat "Check these files for issues" --file setup.py --file requirements.txt --agent workspace

# With context
vscodey-copilot chat "Fix import errors in this file" --file vscodey/copilot/cli.py --context --agent workspace
```

### Fix Specific Issues
```bash
# Error handling
vscodey-copilot chat "Improve error handling in this module" --file vscodey/copilot/cli_core.py --agent workspace

# Performance optimization
vscodey-copilot chat "Optimize this code for better performance" --file vscodey/copilot/config.py --context --agent workspace

# Add type hints
vscodey-copilot chat "Add proper type hints to this code" --file main.py --agent workspace
```

### Python Import Usage
```python
from vscodey import copilot

cli = copilot.CLIPilot(workspace=".", verbose=True)

# Analyze entire workspace
response = cli.handle_chat(
    "Analyze this project and suggest improvements",
    include_context=True,
    agent="workspace",
    model="claude-3.5-sonnet"
)

# Fix specific file issues
response = cli.handle_chat(
    "Fix the linting issues and improve error handling",
    files=["main.py"],
    include_context=True,
    agent="workspace"
)
```

## 3. 🧠 Set Models & Add Features

### Step-by-Step Feature Development

#### Phase 1: Planning with O1
```bash
# Set model for complex reasoning
vscodey-copilot set-model o1

# Design architecture
vscodey-copilot chat "Design architecture for adding a plugin system to this CLI tool" --context --agent workspace
```

#### Phase 2: Implementation with Claude
```bash
# Switch to implementation model
vscodey-copilot set-model claude-3.5-sonnet

# Implement the feature
vscodey-copilot chat "Implement the plugin loader class based on the architecture" --file vscodey/copilot/cli_core.py --agent workspace
```

#### Phase 3: Review with GPT
```bash
# Switch to review model
vscodey-copilot set-model gpt-4.1-2025-04-14

# Review and optimize
vscodey-copilot chat "Review and optimize this plugin implementation" --file vscodey/copilot/plugin_loader.py --agent workspace
```

#### Phase 4: Testing with Gemini
```bash
# Switch to testing model
vscodey-copilot set-model gemini-2.0-flash-001

# Generate tests
vscodey-copilot chat "Generate comprehensive tests for the plugin system" --context --agent workspace
```

#### Phase 5: Documentation with O1-mini
```bash
# Switch to documentation model
vscodey-copilot set-model o1-mini

# Create documentation
vscodey-copilot chat "Create user documentation for the new plugin feature" --context --agent workspace
```

### Python Import Usage - Complete Workflow
```python
from vscodey import copilot

cli = copilot.CLIPilot(workspace=".", verbose=True)

# Phase 1: Architecture Planning
cli.set_model("o1")
architecture = cli.handle_chat(
    "Design a plugin system architecture for this CLI tool",
    include_context=True,
    agent="workspace"
)

# Phase 2: Implementation
cli.set_model("claude-3.5-sonnet")
implementation = cli.handle_chat(
    "Implement the plugin system based on the architecture",
    files=["vscodey/copilot/cli_core.py"],
    include_context=True,
    agent="workspace"
)

# Phase 3: Integration
cli.set_model("gpt-4.1-2025-04-14")
integration = cli.handle_chat(
    "Integrate the plugin system into the CLI interface",
    files=["vscodey/copilot/cli.py", "vscodey/copilot/cli_core.py"],
    agent="workspace"
)

# Phase 4: Testing
cli.set_model("gemini-2.0-flash-001")
testing = cli.handle_chat(
    "Generate comprehensive tests for the plugin system",
    include_context=True,
    agent="workspace"
)

# Phase 5: Documentation
cli.set_model("o1-mini")
documentation = cli.handle_chat(
    "Create API documentation and usage examples",
    include_context=True,
    agent="workspace"
)
```

## 🚀 Quick Start Commands

```bash
# Setup authentication
vscodey-copilot auth login

# Enable MCP browser for research
vscodey-copilot mcp enable brave-search

# Research example
vscodey-copilot chat "Find Python security best practices for 2025" --agent agent

# Analyze project
vscodey-copilot chat "Analyze this project structure" --context --agent workspace

# Fix issues
vscodey-copilot chat "Review and fix issues in this file" --file main.py --agent workspace

# Start feature development
vscodey-copilot set-model o1
vscodey-copilot chat "Design architecture for adding user authentication" --context --agent workspace
```

## 💡 Pro Tips

- **Research**: Use `--agent agent` with MCP browser enabled
- **Analysis**: Use `--context` flag for project-wide analysis  
- **File Work**: Use `--file <path>` for specific file analysis
- **Models**: Switch models based on task complexity:
  - `o1`: Complex reasoning, architecture
  - `claude-3.5-sonnet`: Implementation, detailed coding
  - `gpt-4.1-2025-04-14`: Review, optimization
  - `gemini-2.0-flash-001`: Testing, validation
  - `o1-mini`: Documentation, explanations
- **Interactive**: Use `vscodey-copilot interactive` for ongoing conversations
