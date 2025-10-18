# Documentation Index

Welcome to the JoResa Python Tools documentation! This index will help you find the right document for your needs.

## 📚 Complete Documentation List

### Essential Documents (Start Here!)

| Document | Purpose | Audience |
|----------|---------|----------|
| **[README.md](README.md)** | Project overview, features, setup | Everyone |
| **[QUICKSTART.md](docs/guides/quickstart.md)** | Getting started guide | New users |
| **[SUMMARY.md](SUMMARY.md)** | Project statistics and overview | Managers, stakeholders |

### Technical Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **[ARCHITECTURE.md](docs/architecture/architecture.md)** | System architecture, models, blueprints | Developers |
| **[DIAGRAMS.md](DIAGRAMS.md)** | Visual flows and diagrams | Developers, architects |
| **[DESIGN.md](docs/design/visual-design.md)** | UI/UX design system | Frontend developers |

### Development Guides

| Document | Purpose | Audience |
|----------|---------|----------|
| **[ADDING_TOOLS.md](ADDING_TOOLS.md)** | How to add new tools (with examples) | Developers |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Contribution guidelines | Contributors |
| **[TESTING.md](docs/testing/testing.md)** | Testing strategies and checklist | Developers, QA |
| **[PYCHARM_SETUP.md](PYCHARM_SETUP.md)** | PyCharm IDE setup and usage | Developers |

### Operations & Deployment

| Document | Purpose | Audience |
|----------|---------|----------|
| **[DEPLOYMENT.md](docs/deployment/deploy.md)** | Production deployment guide | DevOps, sysadmins |
| **[.env.example](.env.example)** | Environment variables template | DevOps |

### Legal & Licensing

| Document | Purpose | Audience |
|----------|---------|----------|
| **[LICENSE](LICENSE)** | MIT License | Everyone |

---

# Quick Reference Sections

The following sections provide quick access to essential information for getting started and working with the project.

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize the Database
```bash
python init_db.py
```

This will:
- Create the database tables
- Seed initial tools (Diff Checker, etc.)
- Set up required data structures

### Step 5: Run the Application
```bash
python run.py
```

The application will start at: `http://127.0.0.1:5000`

### First Use
1. Open http://127.0.0.1:5000 in your browser
2. Click "Register" in the top right
3. Fill in your username, email, and password
4. Login with your credentials
5. Start using the tools from the Dashboard

For more detailed setup instructions, see **[QUICKSTART.md](docs/guides/quickstart.md)**.

## 📁 Project Structure

```
joresa-py-tools/
├── .env.example              # Environment configuration template
├── .gitignore               # Git ignore rules
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
├── README.md               # This file - Documentation index
├── config.py               # Application configuration
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
│
├── app/                    # Main application package
│   ├── __init__.py         # App factory and initialization
│   ├── models.py           # Database models (User, Tool, ToolUsage, etc.)
│   │
│   ├── auth/               # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── forms.py        # Login/registration forms
│   │   └── routes.py       # Auth routes (login, register, logout)
│   │
│   ├── main/               # Main blueprint (dashboard, analytics)
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py       # Dashboard and analytics routes
│   │
│   ├── tools/              # Tools blueprint
│   │   ├── __init__.py
│   │   ├── forms.py        # Tool-specific forms
│   │   ├── routes.py       # Tool routes
│   │   ├── rulecard.py     # Rulecard tool implementation
│   │   └── wp_db_compare.py # WordPress DB comparison tool
│   │
│   ├── static/             # Static assets
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript files
│   │
│   └── templates/          # Jinja2 templates
│       ├── base.html       # Base template
│       ├── index.html      # Landing page
│       ├── auth/           # Authentication templates
│       ├── main/           # Dashboard and analytics templates
│       └── tools/          # Tool-specific templates
│
└── docs/                   # Documentation
    ├── README.md           # Documentation overview
    ├── index.md            # Documentation index
    ├── move-log.md         # Documentation reorganization log
    │
    ├── architecture/       # Architecture documentation
    │   └── architecture.md # System architecture and design
    │
    ├── contributing/       # Contribution guides
    │   ├── README.md
    │   └── adding-tools.md # Guide to adding new tools
    │
    ├── deployment/         # Deployment documentation
    │   └── deploy.md       # Production deployment guide
    │
    ├── design/             # Design documentation
    │   └── visual-design.md # UI/UX design guide
    │
    ├── guides/             # User guides
    │   ├── pycharm-setup.md # PyCharm IDE setup
    │   └── quickstart.md    # Quick start guide
    │
    ├── reference/          # Reference documentation
    │   └── index.md
    │
    ├── testing/            # Testing documentation
    │   └── testing.md      # Testing procedures and checklist
    │
    ├── tools/              # Tool-specific documentation
    │   └── wp-db-compare.md # WordPress DB comparison tool docs
    │
    └── archive/            # Archived documentation
        └── *.md            # Previous versions of documentation
```

### Key Files and Directories

- **`run.py`** - Entry point for running the Flask application
- **`init_db.py`** - Initializes the database and seeds initial data
- **`config.py`** - Configuration classes for different environments
- **`app/__init__.py`** - Application factory that creates and configures the Flask app
- **`app/models.py`** - SQLAlchemy database models
- **`app/auth/`** - User authentication and registration
- **`app/main/`** - Main application routes (dashboard, analytics)
- **`app/tools/`** - Tool implementations and routes
- **`app/templates/`** - HTML templates using Jinja2
- **`app/static/`** - CSS, JavaScript, and other static files
- **`docs/`** - Comprehensive documentation (architecture, guides, testing, etc.)

## 🛠️ Adding New Tools

This section provides a quick overview of adding new tools. For a comprehensive guide, see **[ADDING_TOOLS.md](docs/contributing/adding-tools.md)**.

### Quick Steps

1. **Create the Form** (in `app/tools/forms.py`):
```python
class YourToolForm(FlaskForm):
    input_field = TextAreaField('Input', validators=[DataRequired()])
    submit = SubmitField('Process')
```

2. **Create the Route** (in `app/tools/routes.py`):
```python
@bp.route('/your-tool', methods=['GET', 'POST'])
@login_required
def your_tool():
    form = YourToolForm()
    results = None
    
    if form.validate_on_submit():
        # Process the input
        results = process_your_tool(form.input_field.data)
        
        # Record usage for analytics
        record_tool_usage('your_tool')
        
        flash('Processing complete!', 'success')
    
    return render_template('tools/your_tool.html',
                         title='Your Tool',
                         form=form,
                         results=results)
```

3. **Create the Template** (`app/templates/tools/your_tool.html`):
```html
{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h2><i class="bi bi-gear"></i> Your Tool</h2>
        <!-- Add your tool UI here -->
    </div>
</div>
{% endblock %}
```

4. **Register in Database** (add to `init_db.py`):
```python
Tool(
    name='your_tool',
    display_name='Your Tool',
    description='Description of what your tool does.',
    icon='bi-gear',
    route='/tools/your-tool',
    is_active=True
)
```

5. **Run database initialization**:
```bash
python init_db.py
```

### Best Practices
- Always use `@login_required` decorator for tool routes
- Call `record_tool_usage()` to track analytics
- Use flash messages for user feedback
- Validate input with WTForms
- Handle errors gracefully with try-except blocks
- Choose appropriate Bootstrap icons from https://icons.getbootstrap.com/

For detailed examples and advanced features, see the full guide in **[docs/contributing/adding-tools.md](docs/contributing/adding-tools.md)**.

## ⚙️ Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

### Environment Variables

```bash
# Flask secret key for session management
# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here

# Database configuration
# SQLite (default - good for development):
DATABASE_URL=sqlite:///instance/app.db

# PostgreSQL (recommended for production):
# DATABASE_URL=postgresql://username:password@localhost:5432/dbname

# MySQL (alternative):
# DATABASE_URL=mysql://username:password@localhost:3306/dbname

# Flask environment
FLASK_ENV=development  # Use 'production' for production
FLASK_DEBUG=True       # Set to False for production

# Optional settings
SESSION_LIFETIME=86400  # Session timeout in seconds (default: 24 hours)
```

### Configuration Classes

The `config.py` file defines three configuration classes:

- **`Config`** - Base configuration with common settings
- **`DevelopmentConfig`** - Development-specific settings (debug enabled, SQLite)
- **`ProductionConfig`** - Production settings (debug disabled, PostgreSQL recommended)

### Security Best Practices

1. **Never commit `.env` to version control** - It's already in `.gitignore`
2. **Generate a secure SECRET_KEY** for production:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. **Use PostgreSQL or MySQL** in production instead of SQLite
4. **Set `FLASK_DEBUG=False`** in production
5. **Use HTTPS** in production with a reverse proxy (nginx, Apache)

For production deployment details, see **[DEPLOYMENT.md](docs/deployment/deploy.md)**.

## 🍎 Local macOS (zsh) Quick Setup

This section provides a streamlined setup process for macOS users using zsh (default shell on modern macOS).

### Prerequisites
Ensure you have the following installed:
- **Homebrew**: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- **Python 3.8+**: `brew install python3`
- **Git**: `brew install git` (or use Xcode Command Line Tools)

### Complete Setup Commands

```bash
# 1. Clone the repository
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Set up environment configuration
cp .env.example .env
# Edit .env if needed (nano .env or open .env)

# 5. Initialize the database
python init_db.py

# 6. Run the application
python run.py
```

### Quick Development Workflow

```bash
# Start working (from project directory)
cd ~/path/to/joresa-py-tools
source .venv/bin/activate
python run.py

# Open in browser
open http://127.0.0.1:5000

# When done, deactivate virtual environment
deactivate
```

### Troubleshooting on macOS

**Issue: Port 5000 already in use**
```bash
# Check what's using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or use a different port in run.py
```

**Issue: Python version conflicts**
```bash
# Check Python version
python3 --version

# Create venv with specific Python version
python3.9 -m venv .venv
```

**Issue: Permission errors**
```bash
# Fix permission issues
chmod +x run.py init_db.py

# If pip install fails, try with --user flag
pip install --user -r requirements.txt
```

### macOS Development Tools

**Recommended:**
- **PyCharm** - See [PYCHARM_SETUP.md](docs/guides/pycharm-setup.md)
- **VS Code** - Install Python extension
- **iTerm2** - Enhanced terminal
- **Oh My Zsh** - Better zsh experience

**Useful Aliases (add to `~/.zshrc`):**
```bash
# JoResa Tools shortcuts
alias jrt-activate='source ~/path/to/joresa-py-tools/.venv/bin/activate'
alias jrt-run='cd ~/path/to/joresa-py-tools && source .venv/bin/activate && python run.py'
alias jrt-db='cd ~/path/to/joresa-py-tools && source .venv/bin/activate && python init_db.py'
```

After adding aliases, reload your shell:
```bash
source ~/.zshrc
```

### Git Workflow on macOS

See the **Pushing changes (Git)** section below for the recommended Git workflow.

## Pushing changes (Git) — Recommended workflow

Use the following steps to create a branch, commit your changes, and push to GitHub (macOS / zsh):

```bash
# Create a new feature branch off main
git checkout -b feature/short-description

# Work locally, then stage and commit changes
git add .
git commit -m "feat: short description of change"

# Push the new branch and set upstream
git push -u origin feature/short-description

# Open a Pull Request on GitHub from your branch to main
# (request reviews, run CI, and merge when ready)

# Keep your branch up to date while working
git fetch origin
# rebase onto latest main
git rebase origin/main
# or, alternatively
git pull --rebase origin main

# After the PR is merged, clean up local and remote branches
git checkout main
git pull origin main
git branch -d feature/short-description
git push origin --delete feature/short-description
```

Tips:
- Use clear, focused commits and descriptive branch names (e.g. feature/add-diff-export).
- Prefer small PRs for easier review.
- Run tests, linters, and the local app (see Local macOS Quick Setup) before opening a PR.
- Consider using conventional commit prefixes (feat:, fix:, docs:, chore:) to simplify changelogs.

## 🌟 Happy Reading!

This comprehensive documentation suite is here to help you succeed with JoResa Python Tools. Start with what you need, explore what interests you, and build something amazing!

---

**Last Updated**: 2024  
**Documentation Version**: 1.0.0  
**Project Status**: Production Ready