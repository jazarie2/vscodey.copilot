"""
Python module entry point for VSCodey Copilot.
Allows running the CLI via: python -m vscodey.copilot
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
