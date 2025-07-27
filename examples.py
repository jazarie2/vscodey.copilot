#!/usr/bin/env python3
"""
VSCodey Copilot Usage Examples
This script demonstrates all the different ways to use VSCodey Copilot.
"""

import sys
import os

# Add current directory to path for testing
sys.path.insert(0, os.path.dirname(__file__))

def test_package_import():
    """Test package import functionality."""
    print("🧪 Testing package imports...")
    
    # Test main package import
    import vscodey
    print("✅ import vscodey")
    
    # Test subpackage import
    import vscodey.copilot
    print("✅ import vscodey.copilot")
    
    # Test from import
    from vscodey import copilot
    print("✅ from vscodey import copilot")
    
    # Test class imports
    from vscodey.copilot import CLIPilot, ChatInterface, CLIConfig
    print("✅ from vscodey.copilot import CLIPilot, ChatInterface, CLIConfig")
    
    # Test CLI import
    from vscodey.copilot.cli import main
    print("✅ from vscodey.copilot.cli import main")
    
    print("🎉 All imports successful!\n")
    return True


def test_cli_instance():
    """Test creating and using CLIPilot instances."""
    print("🧪 Testing CLIPilot instance creation...")
    
    from vscodey import copilot
    
    # Create instance with default settings
    cli = copilot.CLIPilot()
    print("✅ cli = copilot.CLIPilot()")
    
    # Create instance with custom workspace
    cli_custom = copilot.CLIPilot(workspace=".", verbose=True)
    print("✅ cli_custom = copilot.CLIPilot(workspace='.', verbose=True)")
    
    # Check instance attributes
    print(f"   Workspace: {cli.workspace}")
    print(f"   Verbose: {cli.verbose}")
    
    print("🎉 Instance creation successful!\n")
    return True


def demonstrate_usage_patterns():
    """Demonstrate different usage patterns."""
    print("📚 VSCodey Copilot Usage Patterns")
    print("=" * 50)
    
    print("1️⃣ Command Line Usage:")
    print("   vscodey-copilot chat 'Hello world'")
    print("   vscodey-copilot interactive")
    print("   vscodey-copilot auth login")
    print("")
    
    print("2️⃣ Alternative Command Line:")
    print("   clipilot chat 'Hello world'")
    print("   clipilot interactive")
    print("")
    
    print("3️⃣ Python Module Usage:")
    print("   python -m vscodey.copilot chat 'Hello world'")
    print("   python -m vscodey.copilot interactive")
    print("")
    
    print("4️⃣ Direct Script Usage:")
    print("   python main.py chat 'Hello world'")
    print("   python main.py interactive")
    print("")
    
    print("5️⃣ Python Import Usage:")
    print("   from vscodey import copilot")
    print("   cli = copilot.CLIPilot()")
    print("   # cli.handle_chat('Hello world')")
    print("   # cli.start_interactive()")
    print("")


def main():
    """Main function to run all tests."""
    print("🚀 VSCodey Copilot - Usage Examples & Tests")
    print("=" * 60)
    print()
    
    try:
        # Test imports
        test_package_import()
        
        # Test instance creation
        test_cli_instance()
        
        # Show usage patterns
        demonstrate_usage_patterns()
        
        print("✅ All tests passed!")
        print("\n🎉 VSCodey Copilot is ready to use!")
        print("\n📋 Quick Start:")
        print("1. Setup: vscodey-copilot setup")
        print("2. Chat: vscodey-copilot chat 'Hello!'")
        print("3. Interactive: vscodey-copilot interactive")
        
        return 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
