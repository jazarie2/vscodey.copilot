#!/usr/bin/env python3
"""
CLI entry point for VSCodey Copilot - Command Line Interface for Copilot Chat
Run GitHub Copilot Chat functionality without VSCode.
"""

import argparse
import sys

from .cli_core import CLIPilot


def main():
    """Main entry point for VSCodey Copilot CLI."""
    parser = argparse.ArgumentParser(
        description="VSCodey Copilot - Run GitHub Copilot Chat without VSCode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vscodey-copilot auth login                           # Login with GitHub OAuth
  vscodey-copilot auth status                          # Check authentication status
  vscodey-copilot chat "How do I create a Python function?"
  vscodey-copilot chat "Explain this code" --file main.py
  vscodey-copilot chat "Fix this bug" --file src/app.py --context
  vscodey-copilot chat "Hello" --model claude-3.5-sonnet --agent workspace
  vscodey-copilot interactive --model o1-mini --agent terminal
  vscodey-copilot list-models                          # List available models
  vscodey-copilot set-model claude-3.5-sonnet         # Set default model
  vscodey-copilot list-agents                          # List available agents
  vscodey-copilot set-agent workspace                  # Set default agent
  vscodey-copilot mcp list                             # List MCP servers
  vscodey-copilot mcp enable filesystem               # Enable MCP server
  vscodey-copilot mcp disable github                   # Disable MCP server
  vscodey-copilot setup --token <your-token>          # Manual token setup
  vscodey-copilot --help

Python Module Usage:
  python -m vscodey.copilot chat "Hello world"
  python -m vscodey.copilot interactive
        """,
    )

    parser.add_argument("--version", action="version", version="VSCodey Copilot 1.0.0")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument(
        "--workspace",
        help="Workspace directory (default: current directory)",
        default=".",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Authentication command
    auth_parser = subparsers.add_parser("auth", help="GitHub authentication management")
    auth_subparsers = auth_parser.add_subparsers(
        dest="auth_command", help="Authentication commands"
    )

    # Auth login command
    login_parser = auth_subparsers.add_parser("login", help="Login with GitHub OAuth")
    login_parser.add_argument("--client-id", help="Custom GitHub OAuth client ID")

    # Auth status command
    auth_subparsers.add_parser(
        "status", help="Check authentication status"
    )

    # Auth logout command
    auth_subparsers.add_parser(
        "logout", help="Remove stored authentication"
    )

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Send a chat message to Copilot")
    chat_parser.add_argument("message", help="The message to send to Copilot")
    chat_parser.add_argument(
        "--file", "-f", help="File to include as context", action="append"
    )
    chat_parser.add_argument(
        "--context", "-c", action="store_true", help="Include workspace context"
    )
    chat_parser.add_argument(
        "--agent", help="Specific agent to use (workspace, vscode, etc.)"
    )
    chat_parser.add_argument(
        "--model", "-m", help="Specific model to use (e.g., claude-3.5-sonnet, o1-mini)"
    )

    # Interactive command
    interactive_parser = subparsers.add_parser(
        "interactive", help="Start interactive chat session"
    )
    interactive_parser.add_argument("--agent", help="Specific agent to use")
    interactive_parser.add_argument("--model", "-m", help="Specific model to use")

    # Model management commands
    subparsers.add_parser(
        "list-models", help="List available models"
    )

    set_model_parser = subparsers.add_parser("set-model", help="Set default model")
    set_model_parser.add_argument("model_id", help="Model ID to set as default")

    # Agent management commands
    subparsers.add_parser(
        "list-agents", help="List available agents"
    )

    set_agent_parser = subparsers.add_parser("set-agent", help="Set default agent")
    set_agent_parser.add_argument("agent_id", help="Agent ID to set as default")

    # MCP management commands
    mcp_parser = subparsers.add_parser(
        "mcp", help="Manage MCP (Model Context Protocol) servers"
    )
    mcp_subparsers = mcp_parser.add_subparsers(dest="mcp_command", help="MCP commands")

    # MCP list command
    mcp_subparsers.add_parser("list", help="List MCP servers")

    # MCP enable command
    mcp_enable_parser = mcp_subparsers.add_parser("enable", help="Enable an MCP server")
    mcp_enable_parser.add_argument("server_id", help="MCP server ID to enable")

    # MCP disable command
    mcp_disable_parser = mcp_subparsers.add_parser(
        "disable", help="Disable an MCP server"
    )
    mcp_disable_parser.add_argument("server_id", help="MCP server ID to disable")

    # Setup command (for manual token setup)
    setup_parser = subparsers.add_parser(
        "setup", help="Setup VSCodey Copilot configuration manually"
    )
    setup_parser.add_argument("--token", help="GitHub Copilot token")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        clipilot = CLIPilot(
            workspace=args.workspace, verbose=args.verbose, config_path=args.config
        )

        if args.command == "auth":
            if not args.auth_command:
                auth_parser.print_help()
                return 1

            if args.auth_command == "login":
                return clipilot.handle_auth_login(
                    client_id=getattr(args, "client_id", None)
                )
            elif args.auth_command == "status":
                return clipilot.handle_auth_status()
            elif args.auth_command == "logout":
                return clipilot.handle_auth_logout()

        elif args.command == "chat":
            return clipilot.handle_chat(
                message=args.message,
                files=args.file or [],
                include_context=args.context,
                agent=args.agent,
                model=args.model,
            )
        elif args.command == "interactive":
            return clipilot.start_interactive(agent=args.agent, model=args.model)
        elif args.command == "list-models":
            return clipilot.list_models()
        elif args.command == "set-model":
            return clipilot.set_model(args.model_id)
        elif args.command == "list-agents":
            return clipilot.list_agents()
        elif args.command == "set-agent":
            return clipilot.set_agent(args.agent_id)
        elif args.command == "mcp":
            if not args.mcp_command:
                mcp_parser.print_help()
                return 1

            if args.mcp_command == "list":
                return clipilot.list_mcp_servers()
            elif args.mcp_command == "enable":
                return clipilot.manage_mcp_server("enable", args.server_id)
            elif args.mcp_command == "disable":
                return clipilot.manage_mcp_server("disable", args.server_id)
        elif args.command == "setup":
            return clipilot.setup(token=args.token)
        else:
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 130
    except Exception as e:
        if args.verbose:
            import traceback

            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
