"""
VSCodey package - GitHub Copilot Chat for Command Line
"""

__version__ = "1.0.0"
__author__ = "VSCodey Team"
__description__ = "GitHub Copilot Chat for Command Line"

# Make copilot submodule available for import
from . import copilot

__all__ = ['copilot']
