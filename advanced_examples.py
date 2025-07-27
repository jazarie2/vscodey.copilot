#!/usr/bin/env python3
"""
Advanced VSCodey Copilot Examples
Demonstrates practical usage scenarios including MCP browser, workspace analysis, and model switching.
"""

import sys
import os

# Add current directory to path for testing
sys.path.insert(0, os.path.dirname(__file__))

def example_1_mcp_browser_research():
    """
    Example 1: Using MCP Browser to ask questions that require web research
    This demonstrates using the browser MCP to search for information online.
    """
    print("🌐 Example 1: MCP Browser Research")
    print("=" * 50)
    
    print("# Scenario: Research latest Python best practices")
    print()
    
    # Command line examples
    print("📱 Command Line Usage:")
    print("# Enable browser MCP server first")
    print("vscodey-copilot mcp enable brave-search")
    print()
    
    print("# Ask questions that require web research")
    print('vscodey-copilot chat "What are the latest Python 3.12 features and best practices?" --agent agent')
    print('vscodey-copilot chat "Find recent security vulnerabilities in Python packages" --agent agent')
    print('vscodey-copilot chat "What are the current FastAPI vs Django performance comparisons?" --agent agent')
    print()
    
    # Python import usage
    print("🐍 Python Import Usage:")
    print("""
from vscodey import copilot

# Create CLI instance
cli = copilot.CLIPilot(verbose=True)

# First enable the browser MCP server
cli.manage_mcp_server("enable", "brave-search")

# Ask research questions that need web search
response = cli.handle_chat(
    message="What are the latest security best practices for Python web applications?",
    agent="agent",  # Agent mode uses MCP tools
    model="claude-3.5-sonnet"
)

# Research specific technologies
response = cli.handle_chat(
    message="Compare the latest versions of FastAPI, Django, and Flask for 2025",
    agent="agent",
    model="gpt-4.1-2025-04-14"
)

# Find documentation and tutorials
response = cli.handle_chat(
    message="Find the best Python async/await tutorials and examples",
    agent="agent"
)
""")
    print()


def example_2_workspace_file_analysis():
    """
    Example 2: Using workspace/file analysis to identify and fix issues
    This demonstrates analyzing project files and fixing problems.
    """
    print("📁 Example 2: Workspace & File Analysis")
    print("=" * 50)
    
    print("# Scenario: Analyze project and fix issues")
    print()
    
    # Command line examples
    print("📱 Command Line Usage:")
    print()
    
    print("# 1. Analyze entire project structure")
    print('vscodey-copilot chat "Analyze this project structure and identify potential issues" --context --agent workspace')
    print()
    
    print("# 2. Analyze specific files for problems")
    print('vscodey-copilot chat "Review this code for bugs and improvements" --file main.py --agent workspace')
    print('vscodey-copilot chat "Check for security issues" --file vscodey/copilot/github_auth.py --agent workspace')
    print()
    
    print("# 3. Fix specific issues with context")
    print('vscodey-copilot chat "Fix the import errors and optimize the code" --file vscodey/copilot/cli.py --context --agent workspace')
    print('vscodey-copilot chat "Improve error handling in this module" --file vscodey/copilot/cli_core.py --agent workspace')
    print()
    
    print("# 4. Get testing recommendations")
    print('vscodey-copilot chat "Generate unit tests for this module" --file vscodey/copilot/config.py --agent workspace')
    print()
    
    # Python import usage
    print("🐍 Python Import Usage:")
    print("""
from vscodey import copilot
from pathlib import Path

# Create CLI instance with verbose output
cli = copilot.CLIPilot(workspace=".", verbose=True)

# 1. Analyze entire workspace
response = cli.handle_chat(
    message="Analyze this Python project structure and identify potential issues",
    include_context=True,
    agent="workspace",
    model="claude-3.5-sonnet"
)

# 2. Analyze specific files
response = cli.handle_chat(
    message="Review this code for bugs, security issues, and improvements",
    files=["vscodey/copilot/cli.py", "vscodey/copilot/cli_core.py"],
    agent="workspace",
    model="gpt-4.1-2025-04-14"
)

# 3. Fix specific issues
response = cli.handle_chat(
    message="Fix the linting issues and improve error handling in this file",
    files=["main.py"],
    include_context=True,
    agent="workspace"
)

# 4. Get architecture recommendations  
response = cli.handle_chat(
    message="Suggest architectural improvements for better maintainability",
    include_context=True,
    agent="workspace",
    model="o1"  # Use advanced reasoning model
)

# 5. Generate documentation
response = cli.handle_chat(
    message="Generate comprehensive documentation for this module",
    files=["vscodey/copilot/__init__.py"],
    agent="workspace"
)
""")
    print()


def example_3_model_switching_feature_development():
    """
    Example 3: Set different models and use them to add features
    This demonstrates switching between models for different tasks.
    """
    print("🧠 Example 3: Model Switching for Feature Development")
    print("=" * 50)
    
    print("# Scenario: Add a new feature using different AI models for different tasks")
    print()
    
    # Command line examples
    print("📱 Command Line Usage:")
    print()
    
    print("# 1. Use O1 for complex planning and architecture")
    print('vscodey-copilot set-model o1')
    print('vscodey-copilot chat "Design architecture for adding a plugin system to support custom agents" --context --agent workspace')
    print()
    
    print("# 2. Use Claude for detailed implementation")
    print('vscodey-copilot set-model claude-3.5-sonnet')  
    print('vscodey-copilot chat "Implement a plugin loader class with error handling" --file vscodey/copilot/cli_core.py --agent workspace')
    print()
    
    print("# 3. Use GPT for code review and optimization")
    print('vscodey-copilot set-model gpt-4.1-2025-04-14')
    print('vscodey-copilot chat "Review and optimize this implementation" --file vscodey/copilot/plugin_loader.py --agent workspace')
    print()
    
    print("# 4. Use Gemini for testing and validation")
    print('vscodey-copilot set-model gemini-2.0-flash-001')
    print('vscodey-copilot chat "Generate comprehensive tests for the plugin system" --context --agent workspace')
    print()
    
    print("# 5. Use O1-mini for final documentation")
    print('vscodey-copilot set-model o1-mini')
    print('vscodey-copilot chat "Create user documentation for the new plugin feature" --context --agent workspace')
    print()
    
    # Python import usage
    print("🐍 Python Import Usage:")
    print("""
from vscodey import copilot

# Create CLI instance
cli = copilot.CLIPilot(workspace=".", verbose=True)

# Phase 1: Architecture & Planning (Use O1 for complex reasoning)
print("🏗️ Phase 1: Architecture Planning")
cli.set_model("o1")
architecture_response = cli.handle_chat(
    message="Design a plugin system architecture that allows users to create custom agents with hooks into the CLI workflow",
    include_context=True,
    agent="workspace"
)

# Phase 2: Core Implementation (Use Claude for detailed coding)
print("⚙️ Phase 2: Core Implementation")
cli.set_model("claude-3.5-sonnet")
implementation_response = cli.handle_chat(
    message="Implement the plugin loader and manager classes based on the architecture",
    files=["vscodey/copilot/cli_core.py"],
    include_context=True,
    agent="workspace"
)

# Phase 3: Integration (Use GPT for integration and optimization)
print("🔗 Phase 3: Integration")
cli.set_model("gpt-4.1-2025-04-14")
integration_response = cli.handle_chat(
    message="Integrate the plugin system into the main CLI interface and optimize performance",
    files=["vscodey/copilot/cli.py", "vscodey/copilot/cli_core.py"],
    agent="workspace"
)

# Phase 4: Testing (Use Gemini for comprehensive testing)
print("🧪 Phase 4: Testing")
cli.set_model("gemini-2.0-flash-001")
testing_response = cli.handle_chat(
    message="Generate unit tests, integration tests, and example plugins",
    include_context=True,
    agent="workspace"
)

# Phase 5: Documentation (Use O1-mini for clear documentation)
print("📚 Phase 5: Documentation")
cli.set_model("o1-mini")
docs_response = cli.handle_chat(
    message="Create comprehensive documentation including API reference and plugin development guide",
    include_context=True,
    agent="workspace"
)

# Phase 6: Validation (Use agent mode with MCP tools)
print("✅ Phase 6: Validation")
cli.set_model("claude-3.5-sonnet")
cli.manage_mcp_server("enable", "filesystem")
validation_response = cli.handle_chat(
    message="Validate the implementation by reading all modified files and checking for consistency",
    agent="agent"  # Agent mode uses MCP filesystem tools
)
""")
    print()


def example_interactive_workflow():
    """
    Example of an interactive workflow combining all three scenarios.
    """
    print("🔄 Interactive Workflow Example")
    print("=" * 50)
    
    print("# Complete development workflow using interactive mode")
    print()
    
    print("📱 Command Line Interactive Workflow:")
    print("""
# Start interactive session with workspace agent
vscodey-copilot interactive --agent workspace --model claude-3.5-sonnet

# In interactive mode, you can:
# 1. Research: /agent
#    "Research best practices for Python CLI applications"
#    
# 2. Analyze: /context  
#    "Analyze the current project structure"
#    
# 3. Plan: /model o1
#    "Design a feature to add configuration file validation"
#    
# 4. Implement: /model claude-3.5-sonnet
#    "Implement the configuration validation feature"
#    
# 5. Test: /model gemini-2.0-flash-001  
#    "Generate tests for the validation feature"
#    
# 6. Document: /model o1-mini
#    "Create documentation for the new feature"

# Special commands in interactive mode:
# /help      - Show available commands
# /context   - Display workspace information  
# /files     - List relevant files
# /history   - Show conversation history
# /model     - Switch AI model
# /agent     - Switch agent mode
# /clear     - Clear session history
# /exit      - Exit interactive mode
""")


def practical_use_cases():
    """
    Real-world practical examples for common development tasks.
    """
    print("💼 Practical Use Cases")
    print("=" * 50)
    
    print("""
🔍 Research & Discovery:
• "Find the latest security vulnerabilities in FastAPI and how to fix them"
• "Research Python async best practices for 2025"
• "Compare different Python testing frameworks and their pros/cons"

🐛 Bug Fixing & Analysis:
• "Analyze this error log and suggest fixes" --file error.log
• "Find and fix memory leaks in this Python application" --context
• "Review this code for race conditions" --file async_handler.py

🚀 Feature Development:
• "Add JWT authentication to this FastAPI application" --context
• "Implement a caching layer using Redis" --file api_routes.py  
• "Add input validation with Pydantic models" --context

🧪 Testing & Quality:
• "Generate pytest fixtures for this database model" --file models.py
• "Create integration tests for the API endpoints" --context
• "Add type hints to improve code quality" --file utils.py

📚 Documentation:
• "Generate API documentation from this FastAPI code" --context
• "Create a README for this Python package" --context
• "Write docstrings for all functions in this module" --file helpers.py

🔧 Refactoring & Optimization:
• "Refactor this code to use async/await" --file sync_handler.py
• "Optimize database queries in this ORM code" --file database.py
• "Convert this script to use Click for better CLI" --file script.py
""")


def main():
    """Main function to display all examples."""
    print("🚀 VSCodey Copilot - Advanced Examples")
    print("=" * 60)
    print()
    
    # Show all examples
    example_1_mcp_browser_research()
    print("\n" + "="*60 + "\n")
    
    example_2_workspace_file_analysis()
    print("\n" + "="*60 + "\n")
    
    example_3_model_switching_feature_development()
    print("\n" + "="*60 + "\n")
    
    example_interactive_workflow()
    print("\n" + "="*60 + "\n")
    
    practical_use_cases()
    
    print("\n🎉 All examples demonstrated!")
    print("\n💡 Pro Tips:")
    print("• Use --verbose flag to see detailed processing")
    print("• Combine --context with --file for better analysis")  
    print("• Switch models based on task complexity")
    print("• Use agent mode for tasks requiring MCP tools")
    print("• Enable MCP servers based on your needs")
    
    print("\n🔗 Quick Reference:")
    print("• MCP Browser: Enable with 'vscodey-copilot mcp enable brave-search'")
    print("• File Analysis: Use --file and --context flags")
    print("• Model Switching: Use 'vscodey-copilot set-model <model-name>'")
    print("• Interactive Mode: 'vscodey-copilot interactive' for continuous workflow")


if __name__ == "__main__":
    main()
