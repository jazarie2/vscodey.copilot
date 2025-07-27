"""
Interactive session for CLI Pilot.
"""

import os
import sys
from typing import Any, Dict, Optional

from .chat_interface import ChatInterface
from .context_manager import WorkspaceContextManager


class InteractiveSession:
    """Interactive chat session for CLI Pilot."""

    def __init__(
        self,
        chat_interface: ChatInterface,
        context_manager: WorkspaceContextManager,
        agent: Optional[str] = None,
        model: Optional[str] = None,
        verbose: bool = False,
    ):
        """Initialize interactive session.

        Args:
            chat_interface: Chat interface instance
            context_manager: Workspace context manager
            agent: Specific agent to use
            model: Specific model to use
            verbose: Enable verbose logging
        """
        self.chat_interface = chat_interface
        self.context_manager = context_manager
        self.agent = agent
        self.model = model
        self.verbose = verbose
        self.session_active = True

    def run(self) -> int:
        """Run the interactive session.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            self._print_welcome()

            while self.session_active:
                try:
                    user_input = self._get_user_input()

                    if not user_input.strip():
                        continue

                    # Handle special commands
                    if self._handle_special_commands(user_input):
                        continue

                    # Process chat message
                    self._process_message(user_input)

                except KeyboardInterrupt:
                    print("\n\nGoodbye! 👋")
                    break
                except EOFError:
                    print("\n\nSession ended.")
                    break

            return 0

        except Exception as e:
            print(f"Error in interactive session: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def _print_welcome(self):
        """Print welcome message."""
        workspace_path = self.context_manager.workspace_path

        print("=" * 60)
        print("🚀 CLI Pilot - Interactive Chat Session")
        print("=" * 60)
        print(f"Workspace: {workspace_path}")
        if self.agent:
            print(f"Agent: {self.agent}")
        print()
        print("Commands:")
        print("  /help     - Show help")
        print("  /context  - Show workspace context")
        print("  /files    - List workspace files")
        print("  /history  - Show chat history")
        print("  /clear    - Clear chat history")
        print("  /exit     - Exit session")
        print()
        print("Type your message and press Enter to chat with Copilot.")
        print("Press Ctrl+C or type '/exit' to quit.")
        print("=" * 60)
        print()

    def _get_user_input(self) -> str:
        """Get user input with a prompt.

        Returns:
            User input string
        """
        try:
            prompt = "💬 You: "
            return input(prompt)
        except (KeyboardInterrupt, EOFError):
            raise

    def _handle_special_commands(self, user_input: str) -> bool:
        """Handle special commands.

        Args:
            user_input: User input string

        Returns:
            True if command was handled, False otherwise
        """
        command = user_input.strip().lower()

        if command == "/help":
            self._show_help()
            return True

        elif command == "/context":
            self._show_context()
            return True

        elif command == "/files":
            self._show_files()
            return True

        elif command == "/history":
            self._show_history()
            return True

        elif command == "/clear":
            self._clear_history()
            return True

        elif command in ["/exit", "/quit", "/q"]:
            self.session_active = False
            print("Goodbye! 👋")
            return True

        return False

    def _process_message(self, message: str):
        """Process a chat message.

        Args:
            message: The chat message
        """
        print("\n🤖 Copilot: ", end="")

        # Show typing indicator
        if self.verbose:
            print("(thinking...)")

        # Get workspace context for better responses
        try:
            context = {
                "workspace": str(self.context_manager.workspace_path),
                "workspace_info": self.context_manager.get_workspace_context(),
            }
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not gather workspace context: {e}")
            context = {}

        # Send message to chat interface
        response = self.chat_interface.send_message(
            message=message, context=context, agent=self.agent, model=self.model
        )

        # Display response
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            content = response.get("content", "No response received.")
            print(content)

            # Show references if any
            references = response.get("references", [])
            if references:
                print(f"\n📁 References: {', '.join(references)}")

        print()  # Add spacing

    def _show_help(self):
        """Show help information."""
        print("\n📖 CLI Pilot Help")
        print("=" * 40)
        print("Commands:")
        print("  /help     - Show this help message")
        print("  /context  - Show workspace context information")
        print("  /files    - List relevant files in workspace")
        print("  /history  - Show chat history")
        print("  /clear    - Clear chat history")
        print("  /exit     - Exit interactive session")
        print()
        print("Chat Examples:")
        print("  • Explain this code")
        print("  • Create a Python function that validates emails")
        print("  • Fix the bug in my authentication logic")
        print("  • Write tests for the User class")
        print("  • Refactor this function to be more efficient")
        print("  • How do I implement error handling?")
        print()
        print("Tips:")
        print("  • Be specific about what you want to achieve")
        print("  • Mention specific files, functions, or concepts")
        print("  • Ask follow-up questions for clarification")
        print("=" * 40)
        print()

    def _show_context(self):
        """Show workspace context information."""
        print("\n📂 Workspace Context")
        print("=" * 40)

        try:
            context = self.context_manager.get_workspace_context()

            print(f"Path: {context['path']}")

            # Project info
            project_info = context.get("project_info", {})
            if project_info.get("type") != "unknown":
                print(f"Project Type: {project_info['type'].title()}")

            # Git info
            git_info = context.get("git_info", {})
            if git_info.get("available"):
                print(f"Git Branch: {git_info.get('branch', 'Unknown')}")
                if git_info.get("remote"):
                    print(f"Git Remote: {git_info['remote']}")

            # Stats
            stats = context.get("stats", {})
            print(f"Total Files: {stats.get('total_files', 0)}")
            print(f"Total Size: {stats.get('total_size', 0)} bytes")

            # File types
            file_types = stats.get("file_types", {})
            if file_types:
                print("File Types:")
                for ext, count in sorted(
                    file_types.items(), key=lambda x: x[1], reverse=True
                )[:5]:
                    print(f"  {ext}: {count} files")

        except Exception as e:
            print(f"❌ Error gathering context: {e}")

        print("=" * 40)
        print()

    def _show_files(self):
        """Show relevant files in workspace."""
        print("\n📄 Workspace Files")
        print("=" * 40)

        try:
            context = self.context_manager.get_workspace_context()
            files = context.get("files", [])

            if not files:
                print("No relevant files found.")
            else:
                print(f"Showing {len(files)} files:")
                for i, file_info in enumerate(files[:20], 1):  # Limit to 20 files
                    path = file_info.get("path", "Unknown")
                    size = file_info.get("size", 0)
                    language = file_info.get("language", "unknown")

                    size_str = self._format_file_size(size)
                    print(f"  {i:2d}. {path} ({language}, {size_str})")

                if len(files) > 20:
                    print(f"  ... and {len(files) - 20} more files")

        except Exception as e:
            print(f"❌ Error listing files: {e}")

        print("=" * 40)
        print()

    def _show_history(self):
        """Show chat history."""
        print("\n💬 Chat History")
        print("=" * 40)

        history = self.chat_interface.get_session_history()

        if not history:
            print("No chat history available.")
        else:
            for i, entry in enumerate(history[-10:], 1):  # Show last 10 entries
                entry_type = entry.get("type", "unknown")
                timestamp = entry.get("timestamp", 0)

                if entry_type == "request":
                    message = entry.get("message", "")[:60]
                    if len(entry.get("message", "")) > 60:
                        message += "..."
                    print(f"  {i:2d}. You: {message}")

                elif entry_type == "response":
                    content = entry.get("content", "")[:60]
                    if len(entry.get("content", "")) > 60:
                        content += "..."
                    print(f"  {i:2d}. Copilot: {content}")

        print("=" * 40)
        print()

    def _clear_history(self):
        """Clear chat history."""
        self.chat_interface.clear_session_history()
        print("\n✅ Chat history cleared.")
        print()

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
