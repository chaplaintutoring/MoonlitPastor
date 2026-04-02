#!/usr/bin/env python3
"""
Setup script for OpenClaw Shared Memory System
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from file or use default
version = "1.0.0"

setup(
    name="openclaw-shared-memory",
    version=version,
    author="OpenClaw Community",
    author_email="community@openclaw.ai",
    description="Shared memory system for OpenClaw AI agents with permission control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openclaw-shared-memory",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyYAML>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sm-init=scripts.init_system:main",
            "sm-add=scripts.add_memory:main",
            "sm-get=scripts.get_agent_memory:main",
            "sm-audit=scripts.audit_report:main",
            "sm-check=scripts.check_system:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.yaml", "*.yml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/openclaw-shared-memory/issues",
        "Source": "https://github.com/yourusername/openclaw-shared-memory",
        "Documentation": "https://github.com/yourusername/openclaw-shared-memory/blob/main/README.md",
    },
)