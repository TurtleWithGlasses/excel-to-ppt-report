# Contributing to DataDeck

Thank you for your interest in contributing to DataDeck! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if it's already reported in the Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

For feature requests:

1. Check if it's already suggested
2. Create a new issue describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Alternative solutions considered
   - How it benefits users

### Pull Requests

1. **Fork the repository**
```bash
git clone https://github.com/your-username/datadeck.git
cd datadeck
```

2. **Create a branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

3. **Make your changes**
   - Follow the coding standards (see below)
   - Write/update tests
   - Update documentation

4. **Test your changes**
```bash
pytest
black app/
flake8 app/
```

5. **Commit your changes**
```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve bug in report generation"
```

Use conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Build process or auxiliary tool changes

6. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

## Development Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

Quick start:
```bash
python setup_env.py
pip install -r requirements.txt
docker-compose up -d db redis
python run.py
```

## Coding Standards

### Python Style

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use type hints where possible
- Write docstrings for all functions/classes

```python
def process_data(data: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process the input data according to the configuration.
    
    Args:
        data: Input DataFrame containing raw data
        config: Configuration dictionary with processing rules
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If data is empty or config is invalid
    """
    pass
```

### Code Organization

- Keep functions small and focused
- Use meaningful variable names
- Avoid deep nesting (max 3 levels)
- Keep files under 500 lines
- Use helper functions for complex logic

### Testing

- Write unit tests for all new functions
- Write integration tests for API endpoints
- Aim for >80% code coverage
- Use descriptive test names

```python
def test_excel_processor_reads_valid_file():
    """Test that ExcelProcessor can read a valid Excel file."""
    processor = ExcelProcessor()
    result = processor.read_excel_file("test_data.xlsx")
    assert result is not None
```

## Project Structure

When adding new features, follow this structure:

- **Models**: `app/models/` - Database models
- **Schemas**: `app/schemas/` - Pydantic validation schemas
- **Services**: `app/services/` - Business logic
- **API Endpoints**: `app/api/endpoints/` - API routes
- **Tests**: `tests/` - Test files (mirror app structure)

## Documentation

- Update README.md for major features
- Add docstrings to all functions/classes
- Update API examples if endpoints change
- Add inline comments for complex logic

## Review Process

Pull requests will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Code Quality**: Is it clean and maintainable?
4. **Documentation**: Is it well-documented?
5. **Performance**: Does it impact performance?

## Getting Help

- Check the [README.md](README.md) and [SETUP.md](SETUP.md)
- Ask questions in issue comments
- Join our community discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to DataDeck! 🚀

