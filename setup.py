#!/usr/bin/env python3
"""
Setup script for vscodey.copilot package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="vscodey-copilot",
    version="1.0.0",
    author="VSCodey Team",
    author_email="contact@vscodey.dev",
    description="CLI Pilot - GitHub Copilot Chat for Command Line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jazarie2/vscodey.copilot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "vscodey-copilot=vscodey.copilot.cli:main",
            "clipilot=vscodey.copilot.cli:main",
        ],
    },
    keywords="copilot, github, ai, chat, cli, vscode, code-assistant",
    project_urls={
        "Bug Reports": "https://github.com/jazarie2/vscodey.copilot/issues",
        "Source": "https://github.com/jazarie2/vscodey.copilot",
        "Documentation": "https://github.com/jazarie2/vscodey.copilot/blob/main/README.md",
    },
    include_package_data=True,
    zip_safe=False,
)
