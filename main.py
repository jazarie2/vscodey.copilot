#!/usr/bin/env python3
"""
VSCodey Copilot - Simple launcher script
This file provides backward compatibility for running the tool directly.
"""

import sys
import os

# Add the package to the path for development
package_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, package_path)

# Import after path modification
from vscodey.copilot.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())