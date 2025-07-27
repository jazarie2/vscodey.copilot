#!/usr/bin/env python3
"""
VSCodey Copilot - Interactive Demo
Runnable examples demonstrating the three key scenarios:
1. MCP browser research
2. Workspace/file analysis  
3. Model switching for feature development
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n📍 Step {step_num}: {description}")
    print("-" * 40)

def demo_1_mcp_browser():
    """Demonstrate MCP browser research capabilities."""
    print_header("Demo 1: MCP Browser Research")
    
    print("""
🌐 Scenario: Research the latest Python security practices using web search

This demo shows how to use VSCodey Copilot with MCP browser integration
to research topics that require current web information.
""")
    
    print_step(1, "Enable Browser MCP Server")
    print("Command: vscodey-copilot mcp enable brave-search")
    print("📝 This enables web search capabilities for the AI agent")
    
    print_step(2, "Ask Research Questions")
    print("Commands to try:")
    print('• vscodey-copilot chat "What are the latest Python security vulnerabilities in 2025?" --agent agent')
    print('• vscodey-copilot chat "Find current best practices for FastAPI security" --agent agent') 
    print('• vscodey-copilot chat "Research the latest Python async/await patterns" --agent agent')
    
    print_step(3, "Python Import Usage")
    print("""
from vscodey import copilot

# Create CLI instance
cli = copilot.CLIPilot(verbose=True)

# Enable browser MCP
cli.manage_mcp_server("enable", "brave-search")

# Research question requiring web search
response = cli.handle_chat(
    message="What are the latest Python 3.12 security features and best practices?",
    agent="agent",  # Agent mode uses MCP tools
    model="claude-3.5-sonnet"
)
""")

def demo_2_workspace_analysis():
    """Demonstrate workspace and file analysis."""
    print_header("Demo 2: Workspace & File Analysis")
    
    print("""
📁 Scenario: Analyze the current project and fix identified issues

This demo shows how to use VSCodey Copilot to analyze your workspace,
identify problems, and get suggestions for improvements.
""")
    
    print_step(1, "Analyze Project Structure")
    print("Command: vscodey-copilot chat \"Analyze this Python project structure\" --context --agent workspace")
    print("📝 This analyzes the entire project structure and identifies potential issues")
    
    print_step(2, "Review Specific Files")
    print("Commands to try:")
    print('• vscodey-copilot chat "Review this file for bugs and improvements" --file main.py --agent workspace')
    print('• vscodey-copilot chat "Check for security issues" --file vscodey/copilot/cli.py --agent workspace')
    print('• vscodey-copilot chat "Optimize this code" --file setup.py --agent workspace')
    
    print_step(3, "Fix Issues with Context")
    print("Commands to try:")
    print('• vscodey-copilot chat "Fix import errors and improve error handling" --file vscodey/copilot/cli.py --context --agent workspace')
    print('• vscodey-copilot chat "Add proper type hints" --file vscodey/copilot/config.py --agent workspace')
    
    print_step(4, "Python Import Usage")
    print("""
from vscodey import copilot

# Create CLI instance
cli = copilot.CLIPilot(workspace=".", verbose=True)

# Analyze entire workspace
response = cli.handle_chat(
    message="Analyze this project and identify potential improvements",
    include_context=True,
    agent="workspace",
    model="claude-3.5-sonnet"
)

# Review specific files
response = cli.handle_chat(
    message="Review this code for bugs and suggest improvements",
    files=["main.py", "setup.py"],
    agent="workspace"
)
""")

def demo_3_model_switching():
    """Demonstrate model switching for feature development."""
    print_header("Demo 3: Model Switching for Feature Development")
    
    print("""
🧠 Scenario: Add a new configuration validation feature using different AI models

This demo shows how to use different AI models for different phases
of feature development, leveraging each model's strengths.
""")
    
    print_step(1, "Planning Phase - Use O1 for Architecture")
    print("Commands:")
    print("vscodey-copilot set-model o1")
    print('vscodey-copilot chat "Design architecture for adding config file validation" --context --agent workspace')
    print("📝 O1 excels at complex reasoning and architectural planning")
    
    print_step(2, "Implementation Phase - Use Claude for Coding")
    print("Commands:")
    print("vscodey-copilot set-model claude-3.5-sonnet")
    print('vscodey-copilot chat "Implement the config validation class" --file vscodey/copilot/config.py --agent workspace')
    print("📝 Claude excels at detailed implementation and code generation")
    
    print_step(3, "Review Phase - Use GPT for Optimization")
    print("Commands:")
    print("vscodey-copilot set-model gpt-4.1-2025-04-14")
    print('vscodey-copilot chat "Review and optimize this implementation" --file vscodey/copilot/config.py --agent workspace')
    print("📝 GPT-4 excels at code review and optimization")
    
    print_step(4, "Testing Phase - Use Gemini for Test Generation")
    print("Commands:")
    print("vscodey-copilot set-model gemini-2.0-flash-001")
    print('vscodey-copilot chat "Generate comprehensive tests" --context --agent workspace')
    print("📝 Gemini excels at test generation and validation")
    
    print_step(5, "Documentation Phase - Use O1-mini for Docs")
    print("Commands:")
    print("vscodey-copilot set-model o1-mini")
    print('vscodey-copilot chat "Create user documentation for the config validation" --context --agent workspace')
    print("📝 O1-mini excels at clear, concise documentation")
    
    print_step(6, "Python Import Usage - Complete Workflow")
    print("""
from vscodey import copilot

cli = copilot.CLIPilot(workspace=".", verbose=True)

# Phase 1: Architecture (O1)
cli.set_model("o1")
architecture = cli.handle_chat(
    "Design config validation architecture",
    include_context=True, agent="workspace"
)

# Phase 2: Implementation (Claude)
cli.set_model("claude-3.5-sonnet")
implementation = cli.handle_chat(
    "Implement the config validation based on the architecture",
    files=["vscodey/copilot/config.py"], agent="workspace"
)

# Phase 3: Testing (Gemini)
cli.set_model("gemini-2.0-flash-001")
tests = cli.handle_chat(
    "Generate comprehensive tests for config validation",
    include_context=True, agent="workspace"
)

# Phase 4: Documentation (O1-mini)
cli.set_model("o1-mini")
docs = cli.handle_chat(
    "Create documentation for the new feature",
    include_context=True, agent="workspace"
)
""")

def demo_interactive_mode():
    """Demonstrate interactive mode workflow."""
    print_header("Interactive Mode Workflow")
    
    print("""
🔄 Interactive mode allows you to have ongoing conversations and switch
between different modes and models seamlessly.
""")
    
    print_step(1, "Start Interactive Session")
    print("Command: vscodey-copilot interactive --agent workspace --model claude-3.5-sonnet")
    
    print_step(2, "Interactive Commands")
    print("""
In interactive mode, you can use these special commands:

/help      - Show available commands
/context   - Display workspace information
/files     - List relevant files in workspace
/history   - Show conversation history
/model <name> - Switch to different AI model
/agent <name> - Switch to different agent mode
/clear     - Clear conversation history
/exit      - Exit interactive mode

Example interactive session:
> "Analyze the current project structure"
> /model o1
> "Design a plugin architecture for this CLI tool"
> /model claude-3.5-sonnet  
> "Implement the plugin loader class"
> /model gpt-4.1-2025-04-14
> "Review and optimize the implementation"
> /exit
""")

def practical_examples():
    """Show practical real-world examples."""
    print_header("Practical Real-World Examples")
    
    print("""
🎯 Here are practical commands you can run right now:

🔍 RESEARCH & DISCOVERY:
vscodey-copilot mcp enable brave-search
vscodey-copilot chat "Find the latest Python security best practices for 2025" --agent agent

📁 PROJECT ANALYSIS:
vscodey-copilot chat "Analyze this project structure and suggest improvements" --context --agent workspace
vscodey-copilot chat "Review this file for potential issues" --file main.py --agent workspace

🐛 BUG FIXING:
vscodey-copilot chat "Find and fix any bugs in this code" --file vscodey/copilot/cli.py --agent workspace
vscodey-copilot chat "Improve error handling" --file vscodey/copilot/cli_core.py --context --agent workspace

🚀 FEATURE DEVELOPMENT:
vscodey-copilot set-model o1
vscodey-copilot chat "Design a plugin system architecture" --context --agent workspace

vscodey-copilot set-model claude-3.5-sonnet
vscodey-copilot chat "Implement the plugin loader" --file vscodey/copilot/cli_core.py --agent workspace

🧪 TESTING:
vscodey-copilot set-model gemini-2.0-flash-001
vscodey-copilot chat "Generate unit tests for this module" --file vscodey/copilot/config.py --agent workspace

📚 DOCUMENTATION:
vscodey-copilot set-model o1-mini
vscodey-copilot chat "Create comprehensive documentation" --context --agent workspace
""")

def run_live_demo():
    """Run a live demo if the package is available."""
    print_header("Live Demo")
    
    try:
        from vscodey import copilot
        print("✅ VSCodey Copilot package is available!")
        print("\n🧪 Running live test...")
        
        # Test basic functionality
        cli = copilot.CLIPilot(verbose=True)
        print(f"✅ Created CLIPilot instance with workspace: {cli.workspace}")
        
        # Test model listing (if available)
        try:
            print("\n📋 Available functionality:")
            print("• CLI instance creation: ✅")
            print("• Model management: Available")  
            print("• Agent switching: Available")
            print("• MCP server management: Available")
            print("• File analysis: Available")
            print("• Context management: Available")
            
        except Exception as e:
            print(f"⚠️ Some features may require authentication: {e}")
            
        print("\n💡 To get started:")
        print("1. Run: vscodey-copilot setup")
        print("2. Or: vscodey-copilot auth login")
        print("3. Then try: vscodey-copilot chat 'Hello!'")
        
    except ImportError:
        print("❌ VSCodey Copilot package not found.")
        print("💡 To install: python install.py")
        print("💡 Or try: pip install -e .")

def main():
    """Main demo function."""
    print("🚀 VSCodey Copilot - Interactive Demo")
    print("=" * 60)
    print("""
This demo shows three key scenarios:
1. 🌐 MCP Browser Research - Ask questions requiring web search
2. 📁 Workspace Analysis - Analyze and fix project issues  
3. 🧠 Model Switching - Use different AI models for different tasks
""")
    
    print("\n⚡ Choose a demo to run:")
    print("1. MCP Browser Research Demo")
    print("2. Workspace Analysis Demo") 
    print("3. Model Switching Demo")
    print("4. Interactive Mode Demo")
    print("5. Practical Examples")
    print("6. Live Demo (if package installed)")
    print("7. Show All Demos")
    print("0. Exit")
    
    try:
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "1":
            demo_1_mcp_browser()
        elif choice == "2":
            demo_2_workspace_analysis()
        elif choice == "3":
            demo_3_model_switching()
        elif choice == "4":
            demo_interactive_mode()
        elif choice == "5":
            practical_examples()
        elif choice == "6":
            run_live_demo()
        elif choice == "7":
            demo_1_mcp_browser()
            demo_2_workspace_analysis()
            demo_3_model_switching()
            demo_interactive_mode()
            practical_examples()
            run_live_demo()
        elif choice == "0":
            print("👋 Goodbye!")
            return 0
        else:
            print("❌ Invalid choice. Please try again.")
            return main()
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
        return 0
    
    print("\n🎉 Demo completed!")
    print("\n💡 Try running these commands in your terminal to get started!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
