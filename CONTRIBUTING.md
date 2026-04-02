# Contributing to OpenClaw Shared Memory System

Thank you for your interest in contributing to the OpenClaw Shared Memory System! This document provides guidelines and instructions for contributing.

## 🎯 How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an issue with:
- **Clear description** of the bug
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, OpenClaw version)
- **Screenshots or logs** if applicable

### Suggesting Features
We welcome feature suggestions! Please create an issue with:
- **Clear description** of the feature
- **Use case** and why it's valuable
- **Potential implementation** ideas
- **Alternatives considered**

### Submitting Code Changes
1. **Fork** the repository
2. **Create a branch** for your feature/fix
3. **Make your changes**
4. **Add tests** if applicable
5. **Update documentation**
6. **Submit a Pull Request**

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- OpenClaw (for testing integration)

### Installation
```bash
# Clone your fork
git clone https://github.com/yourusername/openclaw-shared-memory.git
cd openclaw-shared-memory

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_permissions.py

# Run with coverage
python -m pytest --cov=scripts tests/
```

### Code Style
We use:
- **Black** for code formatting
- **Flake8** for linting
- **PEP 8** style guide

```bash
# Format code
black scripts/

# Check linting
flake8 scripts/
```

## 📁 Project Structure

```
openclaw-shared-memory/
├── scripts/              # Core Python scripts
│   ├── init_system.py
│   ├── add_memory.py
│   ├── get_agent_memory.py
│   ├── audit_report.py
│   ├── check_system.py
│   ├── create_agent_permissions.py
│   └── demo_test.py
├── references/           # Documentation
│   └── quick-start.md
├── tests/               # Test files
├── .github/             # GitHub Actions
├── SKILL.md            # OpenClaw skill definition
├── README.md           # Project documentation
├── LICENSE             # MIT License
├── requirements.txt    # Python dependencies
├── setup.py           # Installation script
└── .gitignore         # Git ignore rules
```

## 🔧 Code Guidelines

### Python Code
- Follow PEP 8 style guide
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Include type hints where applicable
- Handle exceptions gracefully

### Documentation
- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Update CHANGELOG.md for significant changes

### Testing
- Write tests for new features
- Ensure existing tests pass
- Test edge cases
- Include integration tests for OpenClaw compatibility

## 🧪 Testing with OpenClaw

To test integration with OpenClaw:

```bash
# Install the skill in OpenClaw
mkdir -p ~/.openclaw/skills/
cp -r . ~/.openclaw/skills/shared-memory-system

# Test initialization
cd ~/.openclaw/skills/shared-memory-system
python scripts/init_system.py

# Run the demo
python scripts/demo_test.py
```

## 📝 Pull Request Process

1. **Ensure tests pass** and code style is consistent
2. **Update documentation** for any changes
3. **Add to CHANGELOG.md** if applicable
4. **Describe changes** in the PR description
5. **Link related issues** in the PR
6. **Request review** from maintainers

### PR Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] OpenClaw integration tested

## 🏆 Recognition

All contributors will be recognized in:
- **README.md** contributors section
- **Release notes**
- **Project documentation**

## ❓ Questions?

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Community**: Join the OpenClaw Discord community

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the OpenClaw ecosystem! 🦊