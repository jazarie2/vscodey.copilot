#!/usr/bin/env python3
"""
Demo script for VSCodey Copilot - Real GitHub Copilot Integration
Demonstrates authentication and chat functionality using the actual GitHub Copilot API.
"""

import sys
import os
from pathlib import Path

# Add the package to the path
sys.path.insert(0, str(Path(__file__).parent))

from vscodey.copilot import ChatInterface, CLIConfig


def main():
    """Main demo function."""
    print("🤖 VSCodey Copilot - Real GitHub Copilot API Demo")
    print("=" * 50)
    
    # Initialize configuration
    config = CLIConfig()
    
    # Initialize chat interface with verbose output
    chat = ChatInterface(config, verbose=True)
    
    print("\n📋 Available functionality:")
    print("✅ Real GitHub OAuth authentication")
    print("✅ Copilot token exchange")
    print("✅ Live GitHub Copilot API calls")
    print("✅ File analysis and workspace context")
    print("✅ Cross-platform compatibility (Windows/Unix/Mac)")
    
    # Step 1: Authentication
    print("\n🔑 Step 1: GitHub Copilot Authentication")
    print("This will open your browser for GitHub OAuth...")
    
    try:
        authenticated = chat.authenticate()
        
        if not authenticated:
            print("\n❌ Authentication failed!")
            print("Please ensure you have:")
            print("- Active internet connection")
            print("- GitHub account with Copilot subscription")
            print("- Browser access for OAuth flow")
            return
        
        print("\n✅ Authentication successful!")
        
    except KeyboardInterrupt:
        print("\n👋 Authentication cancelled by user")
        return
    except Exception as e:
        print(f"\n❌ Authentication error: {e}")
        return
    
    # Step 2: Test basic chat
    print("\n💬 Step 2: Testing Chat Functionality")
    
    # Simple greeting
    print("\n🔹 Sending: 'Hello, can you help me with Python?'")
    response = chat.send_message("Hello, can you help me with Python?")
    
    if response.get("error"):
        print(f"❌ Error: {response['error']}")
        if not response.get("available", True):
            print("   The GitHub Copilot API is not available.")
            print("   This could be due to:")
            print("   - No active Copilot subscription")
            print("   - API quota exceeded")
            print("   - Network connectivity issues")
            return
    else:
        print("✅ Response received:")
        print(f"   {response.get('content', 'No content')[:200]}...")
        print(f"   Model: {response.get('metadata', {}).get('model', 'unknown')}")
    
    # Step 3: Test with workspace context
    print("\n🏗️ Step 3: Testing Workspace Analysis")
    
    workspace_context = {
        "workspace": str(Path.cwd()),
        "files": [
            {
                "path": "demo.py",
                "content": open(__file__).read() if os.path.exists(__file__) else "# Demo file",
                "size": os.path.getsize(__file__) if os.path.exists(__file__) else 0
            }
        ]
    }
    
    print("🔹 Sending: 'Analyze this Python demo file'")
    response = chat.send_message(
        "Analyze this Python demo file and explain what it does",
        context=workspace_context,
        agent="explain"
    )
    
    if response.get("error"):
        print(f"❌ Error: {response['error']}")
    else:
        print("✅ Analysis response received:")
        print(f"   {response.get('content', 'No content')[:300]}...")
        references = response.get('references', [])
        if references:
            print(f"   Referenced files: {', '.join(references)}")
    
    # Step 4: Test terminal agent
    print("\n🖥️ Step 4: Testing Terminal Agent")
    
    print("🔹 Sending: 'What operating system am I on and show me current directory'")
    response = chat.send_message(
        "What operating system am I on and show me current directory",
        context=workspace_context,
        agent="terminal"
    )
    
    if response.get("error"):
        print(f"❌ Error: {response['error']}")
    else:
        print("✅ Terminal response received:")
        print(f"   {response.get('content', 'No content')[:300]}...")
    
    # Step 5: Show session history
    print("\n📜 Step 5: Session History")
    history = chat.get_session_history()
    print(f"✅ Session contains {len(history)} messages")
    
    for i, msg in enumerate(history[-4:], 1):  # Show last 4 messages
        msg_type = msg.get('type', 'unknown')
        timestamp = msg.get('timestamp', 0)
        if msg_type == 'request':
            content = msg.get('message', '')[:50]
            print(f"   {i}. Request: {content}...")
        elif msg_type == 'response':
            content = msg.get('content', '')[:50]
            print(f"   {i}. Response: {content}...")
    
    # Authentication status
    print("\n🔍 Authentication Status:")
    status = chat.get_authentication_status()
    for key, value in status.items():
        icon = "✅" if value else "❌"
        print(f"   {icon} {key}: {value}")
    
    print("\n🎉 Demo Complete!")
    print("\nNext steps:")
    print("- Use ChatInterface in your own scripts")
    print("- Add file context for code analysis")
    print("- Implement streaming responses")
    print("- Add custom agents for specific tasks")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n💥 Demo error: {e}")
        import traceback
        traceback.print_exc()
