"""
Configuration management for CLI Pilot.
"""

import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class CLIConfig:
    """Manages configuration for CLI Pilot."""

    DEFAULT_CONFIG_DIR = Path.home() / ".clipilot"
    DEFAULT_CONFIG_FILE = "config.json"

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Custom path to configuration file
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self.DEFAULT_CONFIG_DIR / self.DEFAULT_CONFIG_FILE

        self.config_dir = self.config_path.parent
        self._config_data = {}

        self._ensure_config_dir()
        self._load_config()

    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self):
        """Load configuration from file."""
        defaults = self._get_default_config()

        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)

                # Merge with defaults to ensure all keys exist
                self._config_data = self._merge_config(defaults, loaded_config)

                # Save the merged config to ensure it has all the latest structure
                self._save_config()

            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                print("Using default configuration.")
                self._config_data = defaults
                self._save_config()
        else:
            self._config_data = defaults

    def _merge_config(
        self, defaults: Dict[str, Any], loaded: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge loaded config with defaults, preserving existing values.

        Args:
            defaults: Default configuration
            loaded: Loaded configuration

        Returns:
            Merged configuration
        """
        result = defaults.copy()

        for key, value in loaded.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config_data, f, indent=2)
        except IOError as e:
            raise Exception(f"Could not save config to {self.config_path}: {e}")

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": "1.0.0",
            "auth": {"token": None, "token_type": "github_copilot"},
            "chat": {
                "default_agent": "workspace",
                "max_context_size": 4096,
                "temperature": 0.1,
                "default_model": "gpt-4o-mini",
                "available_agents": {
                    "workspace": {
                        "name": "Workspace Agent",
                        "description": "Specializes in workspace-wide operations, file analysis, and project understanding",
                        "icon": "code",
                        "capabilities": [
                            "file_analysis",
                            "workspace_context",
                            "project_structure",
                            "code_navigation",
                        ],
                    },
                    "vscode": {
                        "name": "VS Code Agent",
                        "description": "Helps with VS Code features, extensions, settings, and editor functionality",
                        "icon": "vscode",
                        "capabilities": [
                            "editor_features",
                            "extension_help",
                            "settings_config",
                            "debugging",
                        ],
                    },
                    "terminal": {
                        "name": "Terminal Agent",
                        "description": "Assists with command-line operations, shell commands, and terminal workflows",
                        "icon": "terminal",
                        "capabilities": [
                            "shell_commands",
                            "command_line",
                            "scripting",
                            "process_management",
                        ],
                    },
                    "agent": {
                        "name": "Agent Mode",
                        "description": "Autonomous multi-step task execution with tool calling capabilities",
                        "icon": "copilot",
                        "capabilities": [
                            "autonomous_tasks",
                            "tool_calling",
                            "multi_step_planning",
                            "mcp_integration",
                        ],
                    },
                },
                "available_models": {
                    "gpt-4.1-2025-04-14": {
                        "name": "GPT-4.1",
                        "family": "gpt-4.1",
                        "description": "Latest GPT-4.1 model with enhanced reasoning",
                        "max_tokens": 4096,
                        "supports_tools": True,
                        "supports_vision": True,
                    },
                    "gpt-4o-mini": {
                        "name": "GPT-4o Mini",
                        "family": "gpt-4o-mini",
                        "description": "Fast and efficient model for most tasks",
                        "max_tokens": 16384,
                        "supports_tools": True,
                        "supports_vision": True,
                    },
                    "claude-3.5-sonnet": {
                        "name": "Claude 3.5 Sonnet",
                        "family": "claude-3.5-sonnet",
                        "description": "Anthropic's Claude with excellent code understanding",
                        "max_tokens": 8192,
                        "supports_tools": True,
                        "supports_vision": True,
                    },
                    "claude-3.7-sonnet": {
                        "name": "Claude 3.7 Sonnet",
                        "family": "claude-3.7-sonnet",
                        "description": "Latest Claude model with thinking capabilities",
                        "max_tokens": 8192,
                        "supports_tools": True,
                        "supports_vision": True,
                    },
                    "gemini-2.0-flash-001": {
                        "name": "Gemini 2.0 Flash",
                        "family": "gemini-2.0-flash",
                        "description": "Google's fast and capable Gemini model",
                        "max_tokens": 8192,
                        "supports_tools": True,
                        "supports_vision": True,
                    },
                    "o1": {
                        "name": "OpenAI o1",
                        "family": "o1",
                        "description": "Advanced reasoning model for complex problems",
                        "max_tokens": 32768,
                        "supports_tools": False,
                        "supports_vision": False,
                    },
                    "o1-mini": {
                        "name": "OpenAI o1-mini",
                        "family": "o1-mini",
                        "description": "Smaller reasoning model for faster responses",
                        "max_tokens": 65536,
                        "supports_tools": False,
                        "supports_vision": False,
                    },
                },
            },
            "mcp": {
                "enabled": True,
                "servers": {
                    "filesystem": {
                        "name": "Filesystem MCP Server",
                        "description": "Provides file system operations",
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/"],
                        "type": "stdio",
                        "enabled": True,
                        "capabilities": ["file_read", "file_write", "directory_list"],
                    },
                    "brave-search": {
                        "name": "Brave Search MCP Server",
                        "description": "Web search capabilities via Brave Search",
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                        "type": "stdio",
                        "enabled": False,
                        "env": {"BRAVE_API_KEY": "${env:BRAVE_API_KEY}"},
                        "capabilities": ["web_search", "search_results"],
                    },
                    "github": {
                        "name": "GitHub MCP Server",
                        "description": "GitHub repository operations",
                        "command": "npx",
                        "args": ["-y", "@modelcontextprotocol/server-github"],
                        "type": "stdio",
                        "enabled": False,
                        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"},
                        "capabilities": [
                            "repo_access",
                            "issue_management",
                            "pr_operations",
                        ],
                    },
                },
            },
            "workspace": {
                "include_patterns": [
                    "*.py",
                    "*.js",
                    "*.ts",
                    "*.java",
                    "*.cpp",
                    "*.c",
                    "*.h",
                ],
                "exclude_patterns": [
                    "node_modules/**",
                    ".git/**",
                    "__pycache__/**",
                    "*.pyc",
                ],
                "max_file_size": 1024 * 1024,  # 1MB
            },
            "ui": {"color_output": True, "show_typing_indicator": True},
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'auth.token')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config_data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split(".")
        config = self._config_data

        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]

        # Set the value
        config[keys[-1]] = value
        self._save_config()

    def get_token(self) -> Optional[str]:
        """Get authentication token.

        Returns:
            Authentication token or None
        """
        # Try environment variable first
        token = os.getenv("GITHUB_COPILOT_TOKEN")
        if token:
            return token

        # Try configuration file
        return self.get("auth.token")

    def set_token(self, token: Optional[str]):
        """Set authentication token.

        Args:
            token: Authentication token (or None to remove)
        """
        if token is None:
            # Remove token
            self.set("auth.token", None)
        else:
            self.set("auth.token", token)
            # Also set the token type to indicate it's a GitHub token
            self.set("auth.token_type", "github")
            self.set("auth.authenticated_at", time.time())

    def get_auth_info(self) -> Dict[str, Any]:
        """Get authentication information.

        Returns:
            Authentication info dictionary
        """
        return {
            "token": self.get_token(),
            "token_type": self.get("auth.token_type", "github"),
            "authenticated_at": self.get("auth.authenticated_at"),
            "is_authenticated": self.is_configured(),
        }

    def get_chat_config(self) -> Dict[str, Any]:
        """Get chat configuration.

        Returns:
            Chat configuration dictionary
        """
        return self.get("chat", {})

    def get_workspace_config(self) -> Dict[str, Any]:
        """Get workspace configuration.

        Returns:
            Workspace configuration dictionary
        """
        return self.get("workspace", {})

    def is_configured(self) -> bool:
        """Check if CLI Pilot is properly configured.

        Returns:
            True if configured, False otherwise
        """
        return self.get_token() is not None

    def reset(self):
        """Reset configuration to defaults."""
        self._config_data = self._get_default_config()
        self._save_config()

    def export_config(self, path: str):
        """Export configuration to a file.

        Args:
            path: Path to export file
        """
        export_path = Path(path)
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(self._config_data, f, indent=2)

    def import_config(self, path: str):
        """Import configuration from a file.

        Args:
            path: Path to import file
        """
        import_path = Path(path)
        if not import_path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(import_path, "r", encoding="utf-8") as f:
            imported_config = json.load(f)

        self._config_data.update(imported_config)
        self._save_config()

    def get_available_models(self) -> Dict[str, Any]:
        """Get available models configuration.

        Returns:
            Dictionary of available models
        """
        return self.get("chat.available_models", {})

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model.

        Args:
            model_id: Model identifier

        Returns:
            Model information or None if not found
        """
        models = self.get_available_models()
        return models.get(model_id)

    def set_default_model(self, model_id: str):
        """Set the default model.

        Args:
            model_id: Model identifier
        """
        models = self.get_available_models()
        if model_id not in models:
            raise ValueError(
                f"Unknown model: {model_id}. Available models: {list(models.keys())}"
            )

        self.set("chat.default_model", model_id)

    def get_default_model(self) -> str:
        """Get the default model.

        Returns:
            Default model identifier
        """
        return self.get("chat.default_model", "gpt-4o-mini")

    def list_models(self) -> List[Dict[str, Any]]:
        """List all available models with their information.

        Returns:
            List of model information dictionaries
        """
        models = self.get_available_models()
        model_list = []

        for model_id, model_info in models.items():
            model_data = {
                "id": model_id,
                "name": model_info.get("name", model_id),
                "family": model_info.get("family", "unknown"),
                "description": model_info.get(
                    "description", "No description available"
                ),
                "max_tokens": model_info.get("max_tokens", 4096),
                "supports_tools": model_info.get("supports_tools", False),
                "supports_vision": model_info.get("supports_vision", False),
                "is_default": model_id == self.get_default_model(),
            }
            model_list.append(model_data)

        return model_list

    def get_available_agents(self) -> Dict[str, Any]:
        """Get available agents configuration.

        Returns:
            Dictionary of available agents
        """
        return self.get("chat.available_agents", {})

    def get_agent_info(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent information or None if not found
        """
        agents = self.get_available_agents()
        return agents.get(agent_id)

    def set_default_agent(self, agent_id: str):
        """Set the default agent.

        Args:
            agent_id: Agent identifier
        """
        agents = self.get_available_agents()
        if agent_id not in agents:
            raise ValueError(
                f"Unknown agent: {agent_id}. Available agents: {list(agents.keys())}"
            )

        self.set("chat.default_agent", agent_id)

    def get_default_agent(self) -> str:
        """Get the default agent.

        Returns:
            Default agent identifier
        """
        return self.get("chat.default_agent", "workspace")

    def list_agents(self) -> List[Dict[str, Any]]:
        """List all available agents with their information.

        Returns:
            List of agent information dictionaries
        """
        agents = self.get_available_agents()
        agent_list = []

        for agent_id, agent_info in agents.items():
            agent_data = {
                "id": agent_id,
                "name": agent_info.get("name", agent_id),
                "description": agent_info.get(
                    "description", "No description available"
                ),
                "icon": agent_info.get("icon", "copilot"),
                "capabilities": agent_info.get("capabilities", []),
                "is_default": agent_id == self.get_default_agent(),
            }
            agent_list.append(agent_data)

        return agent_list

    def get_mcp_config(self) -> Dict[str, Any]:
        """Get MCP configuration.

        Returns:
            MCP configuration dictionary
        """
        return self.get("mcp", {})

    def is_mcp_enabled(self) -> bool:
        """Check if MCP is enabled.

        Returns:
            True if MCP is enabled, False otherwise
        """
        return self.get("mcp.enabled", False)

    def get_mcp_servers(self) -> Dict[str, Any]:
        """Get configured MCP servers.

        Returns:
            Dictionary of MCP servers
        """
        return self.get("mcp.servers", {})

    def get_enabled_mcp_servers(self) -> Dict[str, Any]:
        """Get only enabled MCP servers.

        Returns:
            Dictionary of enabled MCP servers
        """
        servers = self.get_mcp_servers()
        return {
            server_id: server_info
            for server_id, server_info in servers.items()
            if server_info.get("enabled", False)
        }

    def list_mcp_servers(self) -> List[Dict[str, Any]]:
        """List all MCP servers with their information.

        Returns:
            List of MCP server information dictionaries
        """
        servers = self.get_mcp_servers()
        server_list = []

        for server_id, server_info in servers.items():
            server_data = {
                "id": server_id,
                "name": server_info.get("name", server_id),
                "description": server_info.get(
                    "description", "No description available"
                ),
                "command": server_info.get("command", ""),
                "args": server_info.get("args", []),
                "type": server_info.get("type", "stdio"),
                "enabled": server_info.get("enabled", False),
                "capabilities": server_info.get("capabilities", []),
                "env": server_info.get("env", {}),
            }
            server_list.append(server_data)

        return server_list

    def enable_mcp_server(self, server_id: str):
        """Enable an MCP server.

        Args:
            server_id: MCP server identifier
        """
        servers = self.get_mcp_servers()
        if server_id not in servers:
            raise ValueError(
                f"Unknown MCP server: {server_id}. Available servers: {list(servers.keys())}"
            )

        self.set(f"mcp.servers.{server_id}.enabled", True)

    def disable_mcp_server(self, server_id: str):
        """Disable an MCP server.

        Args:
            server_id: MCP server identifier
        """
        servers = self.get_mcp_servers()
        if server_id not in servers:
            raise ValueError(
                f"Unknown MCP server: {server_id}. Available servers: {list(servers.keys())}"
            )

        self.set(f"mcp.servers.{server_id}.enabled", False)
