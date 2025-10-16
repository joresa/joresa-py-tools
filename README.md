# JoResa Python Tools

A modular web-based platform for productivity tools with user authentication, analytics dashboard, and extensible architecture.

## Features

- **User Authentication**: Secure login and registration system
- **Dashboard**: Clean interface showing available tools and recent activity
- **Analytics Dashboard**: View usage statistics with interactive charts
  - Most used tools
  - Usage by date
  - Usage by user
- **Diff Checker Tool**: Compare two texts/files with highlighted changes
  - History tracking per user
  - Side-by-side comparison view
  - Detailed diff history
- **Modular Architecture**: Easy to add new tools

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite (easily upgradable to PostgreSQL/MySQL)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python run.py
```

6. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

> **Using PyCharm?** See [PYCHARM_SETUP.md](PYCHARM_SETUP.md) for detailed IDE-specific setup instructions, including debugging and run configurations.

## Usage

### First Time Setup

1. Register a new account from the homepage
2. Login with your credentials
3. Access the dashboard to see available tools

### Diff Checker Tool

1. Navigate to Tools > Diff Checker from the navigation bar
2. Enter two texts in the left and right panels (optional: name them)
3. Click "Compare" to see the differences highlighted
4. View your comparison history by clicking "View History"

### Analytics Dashboard

- Access from the main navigation bar
- View interactive charts showing:
  - Most used tools (last 30 days)
  - Usage trends over time
  - Top users by activity

## Project Structure

```
joresa-py-tools/
├── app/
│   ├── __init__.py          # App factory and initialization
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── main/                # Main blueprint (dashboard, analytics)
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── tools/               # Tools blueprint
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── main/
│   │   └── tools/
│   └── static/              # Static files (CSS, JS)
│       ├── css/
│       └── js/
├── instance/                # Instance folder (SQLite DB)
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── init_db.py              # Database initialization script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Adding New Tools

The system is designed to be modular and extensible. To add a new tool:

1. Create a new route in `app/tools/routes.py`:
```python
@bp.route('/your-tool', methods=['GET', 'POST'])
@login_required
def your_tool():
    # Record tool usage
    record_tool_usage('your_tool')
    
    # Your tool logic here
    return render_template('tools/your_tool.html')
```

2. Create a template in `app/templates/tools/your_tool.html`

3. Add the tool to the database using `init_db.py` or through the Python shell:
```python
from app import create_app, db
from app.models import Tool

app = create_app()
with app.app_context():
    tool = Tool(
        name='your_tool',
        display_name='Your Tool',
        description='Description of your tool',
        icon='bi-icon-name',
        route='/tools/your-tool',
        is_active=True
    )
    db.session.add(tool)
    db.session.commit()
```

## Future Tool Ideas

- Claims task manager
- Workflow helpers
- Document converter
- Text analyzer
- Code formatter

## Configuration

Edit `config.py` to customize:
- Secret key
- Database URI
- Session lifetime

For production, set environment variables:
```bash
export SECRET_KEY='your-secret-key'
export DATABASE_URL='postgresql://user:pass@localhost/dbname'
```

## Local macOS (zsh) Quick Setup

If you're on macOS using zsh, run these commands from the project root to create a virtual environment, install dependencies, initialize the database, and run the app:

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# 3. Install dependencies
pip install -r requirements.txt

# 4. Ensure the instance folder exists (SQLite DB will be created here)
mkdir -p instance

# 5. Initialize the database and seed initial data
python init_db.py

# 6. Run the development server
python run.py
```

Notes:
- The development server runs by default at http://127.0.0.1:5000 and uses Flask's debugger in debug mode. Do not use the development server in production.
- To run with a specific database in development, set the DATABASE_URL environment variable before starting the app, for example:

```bash
export DATABASE_URL='sqlite:////absolute/path/to/instance/app.db'
export SECRET_KEY='replace-with-a-secret'
python run.py
```

- To stop the server, focus its terminal and press CTRL+C. To run the server in the background, consider using a process manager (systemd, launchd, or a WSGI server like gunicorn) for production deployments.

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

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.