# Contributing to JoResa Python Tools

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/joresa-py-tools.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python run.py
```

## Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Comment complex logic

Example:
```python
def generate_diff_html(text1, text2, text1_name='Text 1', text2_name='Text 2'):
    """
    Generate HTML diff between two texts.
    
    Args:
        text1 (str): First text to compare
        text2 (str): Second text to compare
        text1_name (str): Name for first text
        text2_name (str): Name for second text
        
    Returns:
        str: HTML formatted diff output
    """
    # Implementation here
```

## Commit Messages

Use clear, descriptive commit messages:

- Good: `Add password reset functionality`
- Good: `Fix diff highlighting for empty lines`
- Bad: `update stuff`
- Bad: `fix bug`

Format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

## Adding New Tools

See [ADDING_TOOLS.md](ADDING_TOOLS.md) for detailed instructions on adding new tools to the platform.

## Testing

Before submitting a PR:

1. Test all functionality manually
2. Ensure no broken links
3. Check responsive design
4. Test with different browsers
5. Verify database migrations work

## Pull Request Process

1. Update documentation if needed
2. Add your changes to CHANGELOG.md (if it exists)
3. Ensure your code follows the style guide
4. Make sure all tests pass
5. Update README.md if adding new features
6. Request review from maintainers

## What to Contribute

### High Priority
- New tools (see ADDING_TOOLS.md for ideas)
- Bug fixes
- Performance improvements
- Security enhancements
- Documentation improvements

### Good First Issues
- UI/UX improvements
- Adding tool icons
- Improving error messages
- Adding input validation
- Writing tests

### Feature Ideas
- Export functionality (CSV, JSON)
- User preferences/settings
- Dark mode theme
- Email notifications
- API key authentication
- Tool favorites/bookmarks
- Advanced search
- Data visualization improvements

## Reporting Bugs

Use GitHub Issues with the following information:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: Python version, OS, browser
- **Screenshots**: If applicable

Example:
```
Title: Diff checker fails with unicode characters

Description: When comparing texts with unicode characters, the diff checker 
throws an encoding error.

Steps to Reproduce:
1. Go to Diff Checker
2. Enter text with emoji: "Hello 👋"
3. Compare with "Hello"
4. See error

Expected: Diff should display correctly
Actual: 500 Internal Server Error

Environment:
- Python 3.9
- Ubuntu 20.04
- Chrome 120
```

## Feature Requests

Use GitHub Issues with the "enhancement" label:

- Clear description of the feature
- Use case / motivation
- Possible implementation approach
- Examples or mockups (if applicable)

## Code Review

All contributions will be reviewed for:
- Code quality and style
- Security concerns
- Performance impact
- Documentation completeness
- Test coverage
- Breaking changes

## Questions?

- Open a GitHub Discussion
- Check existing documentation
- Review ARCHITECTURE.md for technical details

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone!
