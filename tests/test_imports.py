"""
Tests for VSCodey Copilot package
"""

import pytest
import sys
import os

# Add the package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_package_import():
    """Test that the package can be imported."""
    try:
        import vscodey
        import vscodey.copilot
        from vscodey import copilot
        from vscodey.copilot import CLIPilot
        assert True
    except ImportError as e:
        pytest.fail(f"Package import failed: {e}")


def test_cli_import():
    """Test that the CLI module can be imported."""
    try:
        from vscodey.copilot.cli import main
        assert callable(main)
    except ImportError as e:
        pytest.fail(f"CLI import failed: {e}")


def test_main_launcher():
    """Test that the main launcher script can be imported."""
    try:
        # This tests the main.py file
        exec(open(os.path.join(os.path.dirname(__file__), '..', 'main.py')).read())
        assert True
    except Exception as e:
        pytest.fail(f"Main launcher failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
