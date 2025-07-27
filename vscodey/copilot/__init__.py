"""
VSCodey Copilot - Core functionality for GitHub Copilot Chat without VSCode
"""

__version__ = "1.0.0"
__author__ = "VSCodey Team"
__description__ = "CLI Pilot - GitHub Copilot Chat for Command Line"

# Import main classes for easy access
try:
    from .cli_core import CLIPilot
    from .chat_interface import ChatInterface
    from .config import CLIConfig
    from .context_manager import WorkspaceContextManager
    from .github_auth import GitHubAuth

    __all__ = [
        'CLIPilot', 
        'ChatInterface', 
        'CLIConfig', 
        'WorkspaceContextManager', 
        'GitHubAuth'
    ]
except ImportError:
    # Graceful fallback if some modules are missing
    __all__ = []