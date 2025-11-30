# Contributing to ReportForge

Thank you for your interest in contributing to ReportForge! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Workflow](#development-workflow)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior
- Be respectful and constructive in discussions
- Accept constructive criticism gracefully
- Focus on what is best for the project
- Show empathy towards other contributors

### Unacceptable Behavior
- Harassment, trolling, or discriminatory comments
- Personal attacks or insults
- Publishing others' private information
- Spam or off-topic content

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Python, pandas, and PowerPoint concepts
- Familiarity with GitHub workflow

### Development Setup

1. **Fork the Repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/reportforge.git
   cd "PPT Report Generator"
   ```

3. **Add Upstream Remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/reportforge.git
   ```

4. **Create Virtual Environment**
   ```bash
   python -m venv venv

   # Activate (Windows)
   venv\Scripts\activate

   # Activate (macOS/Linux)
   source venv/bin/activate
   ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt  # If exists
   ```

6. **Verify Setup**
   ```bash
   python scripts/gui.py
   pytest  # If tests exist
   ```

---

## How to Contribute

### Ways to Contribute

#### 1. Report Bugs
- Check if the bug is already reported
- Use the bug report template
- Include detailed reproduction steps
- Provide system information (OS, Python version)

#### 2. Suggest Features
- Check if the feature is already suggested
- Explain the use case clearly
- Describe expected behavior
- Consider implementation complexity

#### 3. Write Documentation
- Fix typos and grammar
- Add examples and tutorials
- Improve existing docs
- Translate documentation

#### 4. Fix Bugs
- Start with "good first issue" labels
- Comment on the issue before starting
- Follow coding standards
- Add tests for the fix

#### 5. Implement Features
- Discuss the feature first in an issue
- Get approval before starting large changes
- Break down into smaller PRs when possible
- Document new functionality

---

## Development Workflow

### 1. Choose an Issue
```bash
# Browse issues on GitHub
# Look for labels: "good first issue", "help wanted", "bug", "enhancement"
# Comment on the issue to claim it
```

### 2. Create Feature Branch
```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch Naming Convention**:
- Features: `feature/descriptive-name`
- Bug fixes: `fix/bug-description`
- Documentation: `docs/what-you-changed`
- Refactoring: `refactor/component-name`

### 3. Make Changes
```bash
# Make your changes
# Test your changes
# Commit frequently with clear messages
```

### 4. Commit Your Changes

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
# Good commit messages
git commit -m "feat: Add bar chart generation support"
git commit -m "fix: Handle missing columns in data processing"
git commit -m "docs: Update API reference for template manager"

# Bad commit messages (avoid these)
git commit -m "Fixed stuff"
git commit -m "WIP"
git commit -m "Changes"
```

### 5. Keep Your Branch Updated
```bash
# Fetch latest changes
git fetch upstream

# Rebase on main
git rebase upstream/main

# Resolve conflicts if any
# Then continue
git rebase --continue
```

### 6. Push Your Changes
```bash
git push origin feature/your-feature-name
```

### 7. Create Pull Request
- Go to GitHub
- Click "New Pull Request"
- Fill in the PR template
- Request reviewers

---

## Coding Standards

### Python Style Guide

Follow **PEP 8** with these additions:

#### Line Length
```python
# Maximum 100 characters per line
# Break long lines logically
result = some_function(
    first_parameter,
    second_parameter,
    third_parameter
)
```

#### Imports
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import pandas as pd
from pptx import Presentation

# Local imports
from template_manager import TemplateManager
from data_processing import load_and_process_data
```

#### Type Hints
```python
from typing import Optional, Dict, Any, List

def create_template(
    name: str,
    client: str,
    description: str = ""
) -> Dict[str, Any]:
    """Create a new template."""
    pass
```

#### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description of function.

    Longer description if needed. Explain what the function does,
    any important details, or caveats.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer

    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

#### Error Handling
```python
# Good
try:
    data = load_data(file_path)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    raise
except PermissionError:
    logger.error(f"Permission denied: {file_path}")
    raise

# Bad
try:
    data = load_data(file_path)
except Exception:
    pass  # Silent failure
```

#### Naming Conventions
```python
# Classes: PascalCase
class TemplateManager:
    pass

# Functions/methods: snake_case
def load_template(template_id):
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_TEMPLATE_DIR = "templates/configs"

# Private methods: _leading_underscore
def _validate_path(path):
    pass
```

### Code Quality Tools

#### Black (Code Formatter)
```bash
# Format all files
black scripts/

# Check without formatting
black --check scripts/
```

#### Flake8 (Linter)
```bash
# Lint all files
flake8 scripts/

# With configuration
flake8 --max-line-length=100 --ignore=E501,W503 scripts/
```

#### MyPy (Type Checker)
```bash
# Type check
mypy scripts/
```

---

## Testing Guidelines

### Writing Tests

#### Test Structure
```python
# tests/test_template_manager.py
import unittest
from template_manager import TemplateManager

class TestTemplateManager(unittest.TestCase):
    """Test suite for TemplateManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = TemplateManager()

    def tearDown(self):
        """Clean up after tests"""
        pass

    def test_create_template(self):
        """Test template creation"""
        template = self.manager.create_template(
            name="Test",
            client="Client"
        )
        self.assertIsNotNone(template)
        self.assertEqual(template['name'], "Test")

    def test_create_template_validation(self):
        """Test template creation with invalid input"""
        with self.assertRaises(ValueError):
            self.manager.create_template(name="", client="")
```

#### Test Coverage
- Aim for >80% code coverage
- Test happy paths and edge cases
- Test error conditions
- Use fixtures for test data

#### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_template_manager.py

# Run with coverage
pytest --cov=scripts --cov-report=html

# Run specific test
pytest tests/test_template_manager.py::TestTemplateManager::test_create_template
```

### Test Data

Create test fixtures in `tests/fixtures/`:
```python
# tests/conftest.py
import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Sample DataFrame for testing"""
    return pd.DataFrame({
        'Company': ['A', 'B', 'C'],
        'Revenue': [1000, 2000, 3000]
    })

@pytest.fixture
def sample_template():
    """Sample template configuration"""
    return {
        "template_id": "test-123",
        "name": "Test Template",
        "client": "Test Client"
    }
```

---

## Documentation

### Documentation Requirements

#### Code Documentation
- All public functions must have docstrings
- All classes must have docstrings
- Complex logic should have inline comments

#### User Documentation
- Update USER_GUIDE.md for user-facing changes
- Add examples for new features
- Update FAQ if needed

#### API Documentation
- Update API_REFERENCE.md for new functions
- Include parameter descriptions
- Provide usage examples

#### Developer Documentation
- Update ARCHITECTURE.md for architectural changes
- Document design decisions
- Update DEVELOPER_GUIDE.md for new workflows

### Documentation Style

#### Markdown Formatting
```markdown
# Main Heading (H1)

## Section Heading (H2)

### Subsection (H3)

**Bold text** for emphasis
*Italic text* for slight emphasis
`code` for inline code
```

#### Code Examples
````markdown
```python
# Include complete, runnable examples
from template_manager import TemplateManager

manager = TemplateManager()
template = manager.create_template("Test", "Client")
```
````

---

## Pull Request Process

### Before Submitting

**Checklist**:
- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] Commits are clear and descriptive
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] Code is self-reviewed

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Fixes #123
Related to #456

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing performed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**
   - Linting passes
   - Tests pass
   - Code coverage maintained

2. **Manual Review**
   - Code quality
   - Design decisions
   - Documentation completeness

3. **Feedback**
   - Address reviewer comments
   - Make requested changes
   - Re-request review

4. **Approval**
   - At least one approval required
   - All discussions resolved
   - CI/CD passes

5. **Merge**
   - Squash commits if many small commits
   - Use merge commit for features
   - Delete branch after merge

### After Merge

- Delete your feature branch
- Update your local main branch
- Close related issues
- Celebrate! 🎉

---

## Priority Areas for Contribution

### High Priority
1. **Chart Generation**
   - Implement bar, line, pie charts
   - Add chart styling options
   - Support multiple data series

2. **Error Handling**
   - Add custom exceptions
   - Improve error messages
   - Add logging framework

3. **Testing**
   - Write unit tests
   - Add integration tests
   - Increase code coverage

4. **Data Processing**
   - Make column mapping flexible
   - Add filtering support
   - Support multiple sheets

### Medium Priority
5. **Performance**
   - Async report generation
   - Caching mechanism
   - Progress indicators

6. **UI Improvements**
   - Better template builder
   - Real-time preview
   - Drag-and-drop components

7. **Documentation**
   - More examples
   - Video tutorials
   - Troubleshooting guides

### Future Ideas
8. **AI Integration**
   - AI-generated insights
   - Smart data analysis
   - Automated summaries

9. **Web Interface**
   - Browser-based app
   - Cloud deployment
   - Team collaboration

---

## Getting Help

### Resources
- **Documentation**: Check `/docs` folder
- **Issues**: Browse existing issues on GitHub
- **Discussions**: GitHub Discussions for questions
- **Examples**: See `templates/configs/` for examples

### Asking Questions
- Search existing issues first
- Provide context and examples
- Include error messages and logs
- Be patient and respectful

---

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project README

Thank you for contributing to ReportForge! 🚀

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
