#!/usr/bin/env python3
"""
Installation script for VSCodey Copilot
"""

import subprocess
import sys


def run_command(command, description):
    """Run a command and print the description."""
    print(f"📦 {description}...")
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Main installation function."""
    print("🚀 VSCodey Copilot Installation")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8 or higher is required. You have Python {sys.version}")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install in development mode
    if run_command("pip install -e .", "Installing VSCodey Copilot in development mode"):
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: vscodey-copilot setup")
        print("2. Or: vscodey-copilot auth login")
        print("3. Start chatting: vscodey-copilot chat 'Hello!'")
        print("\n💡 Alternative commands:")
        print("- clipilot chat 'Hello!'")
        print("- python -m vscodey.copilot chat 'Hello!'")
        print("- python main.py chat 'Hello!'")
        return 0
    else:
        print("\n❌ Installation failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
