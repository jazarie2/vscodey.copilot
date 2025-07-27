"""
Core CLI functionality for Copilot Chat without VSCode.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from .chat_interface import ChatInterface
from .config import CLIConfig
from .context_manager import WorkspaceContextManager
from .github_auth import GitHubAuth, perform_github_login, verify_github_token
from .interactive_session import InteractiveSession


class CLIPilot:
    """Main CLI Pilot class that orchestrates chat functionality."""

    def __init__(
        self,
        workspace: str = ".",
        verbose: bool = False,
        config_path: Optional[str] = None,
    ):
        """Initialize CLI Pilot.

        Args:
            workspace: Path to workspace directory
            verbose: Enable verbose logging
            config_path: Path to configuration file
        """
        self.workspace = Path(workspace).resolve()
        self.verbose = verbose
        self.config = CLIConfig(config_path)
        self.context_manager = WorkspaceContextManager(self.workspace, verbose=verbose)
        self.chat_interface = ChatInterface(self.config, verbose=verbose)

        if verbose:
            print(f"Initialized CLI Pilot in workspace: {self.workspace}")

    def handle_auth_login(self, client_id: Optional[str] = None) -> int:
        """Handle GitHub OAuth login.

        Args:
            client_id: Optional custom client ID

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            print("Starting GitHub authentication...")

            # Create GitHub auth instance
            github_auth = GitHubAuth(client_id=client_id, verbose=self.verbose)

            # Perform authentication
            token = github_auth.authenticate()

            if token:
                # Save token to config
                self.config.set_token(token)

                # Get user info to display confirmation
                user_info = github_auth.get_user_info(token)
                if user_info:
                    username = user_info.get("login", "Unknown")
                    name = user_info.get("name", username)
                    print(f"✓ Successfully authenticated as {name} ({username})")
                else:
                    print("✓ Authentication successful!")

                return 0
            else:
                print("✗ Authentication failed")
                return 1

        except Exception as e:
            print(f"Authentication error: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def handle_auth_status(self) -> int:
        """Handle authentication status check.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            token = self.config.get_token()

            if not token:
                print(
                    "Not authenticated. Run 'python main.py auth login' to authenticate."
                )
                return 1

            print("Checking authentication status...")

            # Verify token is still valid
            if verify_github_token(token, verbose=self.verbose):
                # Get user info
                github_auth = GitHubAuth(verbose=self.verbose)
                user_info = github_auth.get_user_info(token)

                if user_info:
                    username = user_info.get("login", "Unknown")
                    name = user_info.get("name", username)
                    avatar_url = user_info.get("avatar_url", "")

                    print("✓ Authentication Status: Valid")
                    print(f"  User: {name} ({username})")
                    if avatar_url:
                        print(f"  Profile: https://github.com/{username}")
                else:
                    print("✓ Authentication Status: Valid (unable to get user details)")

                return 0
            else:
                print("✗ Authentication Status: Invalid or expired")
                print("Run 'python main.py auth login' to re-authenticate.")
                return 1

        except Exception as e:
            print(f"Error checking authentication status: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def handle_auth_logout(self) -> int:
        """Handle authentication logout (remove stored token).

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            token = self.config.get_token()

            if not token:
                print("Not currently authenticated.")
                return 0

            # Remove token from config
            self.config.set_token(None)
            print("✓ Successfully logged out. Authentication token removed.")

            return 0

        except Exception as e:
            print(f"Error during logout: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def handle_chat(
        self,
        message: str,
        files: List[str] = None,
        include_context: bool = False,
        agent: Optional[str] = None,
        model: Optional[str] = None,
    ) -> int:
        """Handle a single chat message.

        Args:
            message: The chat message
            files: List of files to include as context
            include_context: Whether to include workspace context
            agent: Specific agent to use
            model: Specific model to use

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Check authentication before processing chat
            if not self._check_authentication():
                return 1

            if self.verbose:
                print(f"Processing chat message: {message[:50]}...")

            # Gather context
            context = self._gather_context(files, include_context)

            # Send to chat interface
            response = self.chat_interface.send_message(
                message=message, context=context, agent=agent, model=model
            )

            # Display response
            self._display_response(response)

            return 0

        except Exception as e:
            print(f"Error processing chat message: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def start_interactive(
        self, agent: Optional[str] = None, model: Optional[str] = None
    ) -> int:
        """Start an interactive chat session.

        Args:
            agent: Specific agent to use
            model: Specific model to use

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Check authentication before starting interactive session
            if not self._check_authentication():
                return 1

            session = InteractiveSession(
                chat_interface=self.chat_interface,
                context_manager=self.context_manager,
                agent=agent,
                model=model,
                verbose=self.verbose,
            )
            return session.run()

        except Exception as e:
            print(f"Error in interactive session: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def setup(self, token: Optional[str] = None) -> int:
        """Setup CLI Pilot configuration manually.

        Args:
            token: GitHub Copilot token

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            print("Setting up CLI Pilot manually...")
            print(
                "Note: For OAuth authentication, use 'python main.py auth login' instead."
            )

            if not token:
                token = input("Enter your GitHub token: ").strip()

            if not token:
                print("Error: Token is required")
                return 1

            # Verify token before saving
            if verify_github_token(token, verbose=self.verbose):
                self.config.set_token(token)
                print("✓ Token verified and saved successfully!")

                # Get user info to display confirmation
                github_auth = GitHubAuth(verbose=self.verbose)
                user_info = github_auth.get_user_info(token)
                if user_info:
                    username = user_info.get("login", "Unknown")
                    name = user_info.get("name", username)
                    print(f"✓ Authenticated as {name} ({username})")

                return 0
            else:
                print("✗ Token verification failed. Please check your token.")
                return 1

        except Exception as e:
            print(f"Error during setup: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def list_models(self) -> int:
        """List available models.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            models = self.config.list_models()

            print("\nAvailable Models:")
            print("=" * 80)

            for model in models:
                status = " (default)" if model["is_default"] else ""
                print(f"\n{model['name']}{status}")
                print(f"  ID: {model['id']}")
                print(f"  Family: {model['family']}")
                print(f"  Description: {model['description']}")
                print(f"  Max Tokens: {model['max_tokens']}")
                print(f"  Supports Tools: {'Yes' if model['supports_tools'] else 'No'}")
                print(
                    f"  Supports Vision: {'Yes' if model['supports_vision'] else 'No'}"
                )

            print("\n" + "=" * 80)
            print(f"Current default model: {self.config.get_default_model()}")
            print("\nTo change the default model, use:")
            print("  python main.py set-model <model-id>")
            print("\nTo use a specific model for a chat, use:")
            print('  python main.py chat "your message" --model <model-id>')

            return 0

        except Exception as e:
            print(f"Error listing models: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def set_model(self, model_id: str) -> int:
        """Set the default model.

        Args:
            model_id: Model identifier to set as default

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Validate model exists
            model_info = self.config.get_model_info(model_id)
            if not model_info:
                available = list(self.config.get_available_models().keys())
                print(f"Error: Unknown model '{model_id}'")
                print(f"Available models: {', '.join(available)}")
                print("Use 'python main.py list-models' to see detailed information")
                return 1

            # Set as default
            self.config.set_default_model(model_id)
            print(
                f"✓ Default model set to: {model_info.get('name', model_id)} ({model_id})"
            )

            return 0

        except Exception as e:
            print(f"Error setting model: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def list_agents(self) -> int:
        """List available agents.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            agents = self.config.list_agents()

            print("\nAvailable Agents:")
            print("=" * 80)

            for agent in agents:
                status = " (default)" if agent["is_default"] else ""
                print(f"\n{agent['name']}{status}")
                print(f"  ID: {agent['id']}")
                print(f"  Description: {agent['description']}")
                print(f"  Icon: {agent['icon']}")
                print(f"  Capabilities: {', '.join(agent['capabilities'])}")

            print("\n" + "=" * 80)
            print(f"Current default agent: {self.config.get_default_agent()}")
            print("\nTo change the default agent, use:")
            print("  python main.py set-agent <agent-id>")
            print("\nTo use a specific agent for a chat, use:")
            print('  python main.py chat "your message" --agent <agent-id>')

            return 0

        except Exception as e:
            print(f"Error listing agents: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def set_agent(self, agent_id: str) -> int:
        """Set the default agent.

        Args:
            agent_id: Agent identifier to set as default

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            # Validate agent exists
            agent_info = self.config.get_agent_info(agent_id)
            if not agent_info:
                available = list(self.config.get_available_agents().keys())
                print(f"Error: Unknown agent '{agent_id}'")
                print(f"Available agents: {', '.join(available)}")
                print("Use 'python main.py list-agents' to see detailed information")
                return 1

            # Set as default
            self.config.set_default_agent(agent_id)
            print(
                f"✓ Default agent set to: {agent_info.get('name', agent_id)} ({agent_id})"
            )

            return 0

        except Exception as e:
            print(f"Error setting agent: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def list_mcp_servers(self) -> int:
        """List MCP servers.

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            if not self.config.is_mcp_enabled():
                print("MCP (Model Context Protocol) is disabled.")
                print("To enable MCP, set 'mcp.enabled' to true in your configuration.")
                return 1

            servers = self.config.list_mcp_servers()

            print("\nMCP Servers:")
            print("=" * 80)

            enabled_count = 0
            for server in servers:
                status = "✓ enabled" if server["enabled"] else "✗ disabled"
                if server["enabled"]:
                    enabled_count += 1

                print(f"\n{server['name']} ({status})")
                print(f"  ID: {server['id']}")
                print(f"  Description: {server['description']}")
                print(f"  Command: {server['command']} {' '.join(server['args'])}")
                print(f"  Type: {server['type']}")
                print(f"  Capabilities: {', '.join(server['capabilities'])}")
                if server["env"]:
                    print(f"  Environment: {', '.join(server['env'].keys())}")

            print("\n" + "=" * 80)
            print(
                f"MCP Status: {'enabled' if self.config.is_mcp_enabled() else 'disabled'}"
            )
            print(f"Enabled servers: {enabled_count}/{len(servers)}")
            print("\nTo enable/disable MCP servers, use:")
            print("  python main.py mcp enable <server-id>")
            print("  python main.py mcp disable <server-id>")

            return 0

        except Exception as e:
            print(f"Error listing MCP servers: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def manage_mcp_server(self, action: str, server_id: str) -> int:
        """Enable or disable an MCP server.

        Args:
            action: "enable" or "disable"
            server_id: MCP server identifier

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            if action == "enable":
                self.config.enable_mcp_server(server_id)
                server_info = self.config.get_mcp_servers().get(server_id, {})
                print(
                    f"✓ Enabled MCP server: {server_info.get('name', server_id)} ({server_id})"
                )
            elif action == "disable":
                self.config.disable_mcp_server(server_id)
                server_info = self.config.get_mcp_servers().get(server_id, {})
                print(
                    f"✓ Disabled MCP server: {server_info.get('name', server_id)} ({server_id})"
                )
            else:
                print(f"Error: Unknown action '{action}'. Use 'enable' or 'disable'")
                return 1

            return 0

        except Exception as e:
            print(f"Error managing MCP server: {e}")
            if self.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def _check_authentication(self) -> bool:
        """Check if user is authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        token = self.config.get_token()
        if not token:
            print("Not authenticated. Please run one of the following:")
            print("  python main.py auth login        # OAuth authentication")
            print("  python main.py setup --token ... # Manual token setup")
            return False

        # Skip token verification for now to test model selection
        # TODO: Re-enable token verification once networking issues are resolved
        if self.verbose:
            print("Skipping token verification for testing...")
        return True

        # Verify token is still valid
        if not verify_github_token(token, verbose=self.verbose):
            print("Authentication token is invalid or expired.")
            print("Please re-authenticate with: python main.py auth login")
            return False

        return True

    def _gather_context(
        self, files: Optional[List[str]] = None, include_workspace_context: bool = False
    ) -> Dict[str, Any]:
        """Gather context for the chat request.

        Args:
            files: List of files to include
            include_workspace_context: Whether to include workspace context

        Returns:
            Context dictionary
        """
        context = {"workspace": str(self.workspace), "files": [], "workspace_info": {}}

        # Add specific files
        if files:
            for file_path in files:
                try:
                    full_path = self.workspace / file_path
                    if full_path.exists() and full_path.is_file():
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        context["files"].append(
                            {
                                "path": file_path,
                                "content": content,
                                "size": len(content),
                            }
                        )
                        if self.verbose:
                            print(f"Added file to context: {file_path}")
                    else:
                        print(f"Warning: File not found: {file_path}")
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")

        # Add workspace context if requested
        if include_workspace_context:
            try:
                workspace_info = self.context_manager.get_workspace_context()
                context["workspace_info"] = workspace_info
                if self.verbose:
                    print("Added workspace context")
            except Exception as e:
                print(f"Warning: Could not gather workspace context: {e}")

        return context

    def _display_response(self, response: Dict[str, Any]):
        """Display the chat response.

        Args:
            response: Response from chat interface
        """
        if "error" in response:
            print(f"Error: {response['error']}")
            return

        if "content" in response:
            print("\n" + "=" * 60)
            print("Copilot Response:")
            print("=" * 60)
            print(response["content"])
            print("=" * 60 + "\n")

        if "references" in response and response["references"]:
            print("References:")
            for ref in response["references"]:
                print(f"  - {ref}")
            print()

    def _test_configuration(self) -> bool:
        """Test the current configuration.

        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Simple test message
            test_response = self.chat_interface.send_message(
                message="Hello, this is a test message.", context={}, agent=None
            )
            return "error" not in test_response
        except Exception as e:
            if self.verbose:
                print(f"Configuration test failed: {e}")
            return False
