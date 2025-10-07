# PyCharm Setup Guide

This guide provides detailed instructions for setting up and running the JoResa Python Tools project in PyCharm IDE.

## Prerequisites

- **PyCharm**: Professional or Community Edition (Community Edition is free and sufficient)
  - Download from: https://www.jetbrains.com/pycharm/download/
- **Python**: 3.8 or higher
- **Git**: For cloning the repository

## Initial Setup

### 1. Clone the Repository

#### Option A: Clone via PyCharm
1. Open PyCharm
2. Click **Get from VCS** (or **File > New > Project from Version Control**)
3. Enter the repository URL: `https://github.com/joresa/joresa-py-tools.git`
4. Choose a local directory for the project
5. Click **Clone**

#### Option B: Clone via Command Line
```bash
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools
```

Then open the project in PyCharm:
1. Open PyCharm
2. Click **File > Open**
3. Navigate to the `joresa-py-tools` directory
4. Click **OK**

### 2. Configure Python Interpreter with Virtual Environment

PyCharm can automatically create and manage a virtual environment for your project.

#### Create a New Virtual Environment

1. Open **File > Settings** (Windows/Linux) or **PyCharm > Preferences** (macOS)
2. Navigate to **Project: joresa-py-tools > Python Interpreter**
3. Click the gear icon ⚙️ next to the Python Interpreter dropdown
4. Select **Add Interpreter > Add Local Interpreter**
5. In the dialog:
   - Select **Virtualenv Environment**
   - Choose **New environment**
   - **Location**: The default location (usually `<project_dir>/venv`)
   - **Base interpreter**: Select Python 3.8 or higher
   - Check **Inherit global site-packages**: Leave unchecked
   - Check **Make available to all projects**: Leave unchecked
6. Click **OK**

PyCharm will create the virtual environment and set it as the project interpreter.

#### Use an Existing Virtual Environment

If you've already created a virtual environment manually:

1. Follow steps 1-4 above
2. Select **Existing environment**
3. Click the folder icon and navigate to your `venv/bin/python` (Linux/macOS) or `venv\Scripts\python.exe` (Windows)
4. Click **OK**

### 3. Install Dependencies

Once the virtual environment is configured, install the project dependencies.

#### Option A: Using PyCharm's Terminal
1. Open the PyCharm Terminal: **View > Tool Windows > Terminal**
2. The terminal should automatically activate your virtual environment (you'll see `(venv)` in the prompt)
3. Run:
```bash
pip install -r requirements.txt
```

#### Option B: Using PyCharm's Package Manager
1. Open **File > Settings > Project > Python Interpreter**
2. Click the **+** icon to add packages
3. However, it's recommended to use `requirements.txt` via the terminal for consistency

### 4. Initialize the Database

Before running the application for the first time, you need to initialize the database:

1. Open the PyCharm Terminal
2. Run:
```bash
python init_db.py
```

This will:
- Create the `instance/` directory
- Create the SQLite database (`app.db`)
- Set up all required tables
- Seed the Diff Checker tool

You should see output like:
```
Database initialized successfully!
Diff Checker tool seeded.
```

## Running the Application

### Option 1: Run via PyCharm Configuration (Recommended)

Create a run configuration for easy debugging and running.

#### Create Flask Run Configuration

1. Click **Run > Edit Configurations** (or the dropdown near the Run button)
2. Click the **+** icon and select **Python**
3. Configure as follows:
   - **Name**: `Flask App` (or any name you prefer)
   - **Script path**: Click the folder icon and select `run.py` in your project root
   - **Working directory**: Your project root (usually auto-filled)
   - **Environment variables**: (Optional) Click the folder icon to add:
     - `FLASK_ENV=development`
     - `SECRET_KEY=your-secret-key` (optional for development)
   - **Python interpreter**: Should automatically use your project's virtual environment
   - **Add content roots to PYTHONPATH**: Check this box
   - **Add source roots to PYTHONPATH**: Check this box
4. Click **OK**

#### Run the Application

1. Select your **Flask App** configuration from the dropdown (top-right)
2. Click the green **Run** button ▶️ (or press **Shift+F10**)
3. The application will start, and you'll see output in the Run window:
   ```
   * Serving Flask app 'app'
   * Debug mode: on
   * Running on http://127.0.0.1:5000
   ```
4. Click the URL in the console (hold Ctrl/Cmd and click) to open in your browser

### Option 2: Run via Terminal

1. Open the PyCharm Terminal
2. Ensure your virtual environment is activated (you should see `(venv)`)
3. Run:
```bash
python run.py
```

### Option 3: Right-Click Run

1. Right-click on `run.py` in the Project Explorer
2. Select **Run 'run'**

## Debugging the Application

PyCharm's debugger is one of its most powerful features.

### Set Up Debugging

1. Ensure you have a Flask App run configuration (see above)
2. Set breakpoints by clicking in the gutter (left margin) next to line numbers
   - A red dot will appear where you set a breakpoint
3. Click the **Debug** button 🐞 (or press **Shift+F9**)

### Using the Debugger

When execution hits a breakpoint:
- **Variables**: View in the Debug tool window (bottom)
- **Step Over (F8)**: Execute the current line and move to the next
- **Step Into (F7)**: Step into function calls
- **Step Out (Shift+F8)**: Complete current function and return to caller
- **Resume (F9)**: Continue execution until next breakpoint
- **Evaluate Expression (Alt+F8)**: Evaluate any Python expression in the current context

### Common Debugging Scenarios

#### Debug a Route Handler
1. Open `app/main/routes.py`, `app/tools/routes.py`, or `app/auth/routes.py`
2. Set a breakpoint inside a route function (e.g., `dashboard()`)
3. Start debugging
4. Navigate to that route in your browser
5. Execution will pause at your breakpoint

#### Debug Database Queries
1. Open `app/models.py` or any file with database operations
2. Set breakpoints on SQLAlchemy query lines
3. Debug and inspect the query results in the Variables pane

## Project Structure Overview

Understanding the project structure helps navigate in PyCharm:

```
joresa-py-tools/
├── app/                      # Main application package
│   ├── __init__.py          # Application factory
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
│   ├── static/              # Static files (CSS, JS)
│   │   └── css/
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       ├── auth/
│       ├── main/
│       └── tools/
├── instance/                # Instance folder (created after init_db.py)
│   └── app.db              # SQLite database
├── config.py                # Configuration settings
├── run.py                   # Application entry point
├── init_db.py              # Database initialization
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## PyCharm Tips & Features

### 1. Project Navigation

- **Double-Shift**: Search Everywhere (files, classes, symbols, actions)
- **Ctrl+N** (Cmd+O on macOS): Go to Class
- **Ctrl+Shift+N** (Cmd+Shift+O): Go to File
- **Ctrl+B** (Cmd+B): Go to Declaration/Definition
- **Alt+F7**: Find Usages

### 2. Code Navigation in Flask

- **Ctrl+Click** on a function/class name to jump to its definition
- Navigate between templates and views by Ctrl+Click on template names in `render_template()`
- Navigate to URLs: Ctrl+Click on route decorators

### 3. Code Completion

- PyCharm provides intelligent autocomplete for Flask, SQLAlchemy, and WTForms
- Type `.` after an object to see available methods and attributes
- Use **Ctrl+Space** for basic completion
- Use **Ctrl+Shift+Space** for smart completion

### 4. Refactoring

- **Shift+F6**: Rename (variables, functions, files)
- **Ctrl+Alt+M**: Extract Method
- **Ctrl+Alt+V**: Extract Variable
- **Ctrl+Alt+N**: Inline Variable

### 5. Database Tools (Professional Edition)

PyCharm Professional includes database tools:
1. Open **View > Tool Windows > Database**
2. Click **+** > **Data Source** > **SQLite**
3. Navigate to `instance/app.db`
4. View tables, run queries, and inspect data

For Community Edition, use external tools like DB Browser for SQLite.

### 6. Template Editing

PyCharm provides excellent support for Jinja2 templates:
- Syntax highlighting
- Code completion for variables passed to templates
- Navigate to template definitions from `render_template()` calls

### 7. Version Control Integration

- **Alt+9**: Open Git tool window
- **Ctrl+K**: Commit changes
- **Ctrl+Shift+K**: Push commits
- **Ctrl+T**: Update project (pull)
- View history, compare versions, and resolve conflicts within PyCharm

### 8. TODO Comments

Add TODO comments in your code:
```python
# TODO: Implement email verification
# FIXME: Handle edge case for empty input
```

View all TODOs: **View > Tool Windows > TODO**

## Common Tasks

### Add a New Python Package

1. Open the Terminal in PyCharm
2. Run:
```bash
pip install package-name
```
3. Update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

Or use PyCharm's package manager:
1. **File > Settings > Project > Python Interpreter**
2. Click **+** icon
3. Search and install the package

### Run Database Migrations

If you make changes to models:
1. Delete the database:
```bash
rm -rf instance/
```
2. Re-initialize:
```bash
python init_db.py
```

For production, consider using Flask-Migrate for proper migrations.

### View Application Logs

- Console output appears in the Run/Debug window
- Flask logs requests and errors by default in debug mode
- Check for tracebacks when errors occur

### Test the Application Manually

1. Start the application (Run or Debug)
2. Open http://127.0.0.1:5000 in your browser
3. Register a new account
4. Test features:
   - Login/Logout
   - Dashboard
   - Diff Checker tool
   - Analytics dashboard
   - View history

## Troubleshooting

### Problem: Virtual Environment Not Activating

**Solution**:
- In PyCharm Terminal, the venv should activate automatically
- If not, manually activate:
  - **Windows**: `venv\Scripts\activate`
  - **Linux/macOS**: `source venv/bin/activate`
- Or reconfigure the Python interpreter in PyCharm settings

### Problem: Module Import Errors

**Solution**:
1. Ensure the project root is marked as **Sources Root**:
   - Right-click on the project root folder
   - Select **Mark Directory as > Sources Root**
2. Check that your run configuration has:
   - ✓ Add content roots to PYTHONPATH
   - ✓ Add source roots to PYTHONPATH

### Problem: Database Errors (Table doesn't exist)

**Solution**:
```bash
rm -rf instance/
python init_db.py
```

### Problem: Port 5000 Already in Use

**Solution**:
1. Open `run.py`
2. Change the port:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use a different port
```

### Problem: Templates Not Found

**Solution**:
- Ensure you're running from the project root directory
- Check the working directory in your run configuration
- Verify template files exist in `app/templates/`

### Problem: Static Files Not Loading

**Solution**:
- Hard refresh your browser: **Ctrl+Shift+R** (Cmd+Shift+R)
- Clear browser cache
- Check that `app/static/` directory exists
- Ensure Flask is running in debug mode

### Problem: PyCharm Doesn't Recognize Flask

**Solution**:
1. Ensure Flask is installed in your virtual environment
2. Invalidate caches: **File > Invalidate Caches / Restart**
3. Rebuild the project index

### Problem: Debugging Doesn't Stop at Breakpoints

**Solution**:
- Ensure you're using the **Debug** button (🐞), not the Run button
- Check that breakpoints are enabled (red dots, not gray)
- Verify the debugger is attached (you'll see the debug toolbar)

## Environment Variables

For development, you can set environment variables in your run configuration:

1. **Run > Edit Configurations**
2. In **Environment variables**, add:
   - `SECRET_KEY=your-development-secret-key`
   - `DATABASE_URL=sqlite:///instance/app.db` (default)
   - `FLASK_ENV=development`

For production, use a `.env` file (see `.env.example`).

## Running Tests

Currently, the project focuses on manual testing. To add automated tests:

1. Create a `tests/` directory
2. Write tests using pytest or unittest
3. Run tests via PyCharm:
   - Right-click on the `tests/` folder
   - Select **Run 'pytest in tests'** or **Run 'Unittests in tests'**

## Additional Resources

### Flask Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### PyCharm Resources
- [PyCharm Documentation](https://www.jetbrains.com/pycharm/learn/)
- [PyCharm Keyboard Shortcuts](https://www.jetbrains.com/help/pycharm/mastering-keyboard-shortcuts.html)
- [Debugging Flask Apps in PyCharm](https://www.jetbrains.com/help/pycharm/debugging-flask-applications.html)

### Project Documentation
- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

## Next Steps

After setting up PyCharm:

1. **Explore the code**: Use PyCharm's navigation features to understand the codebase
2. **Try the debugger**: Set breakpoints and step through the code
3. **Make changes**: Modify templates, add features, or fix bugs
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines

## Questions or Issues?

If you encounter problems:
1. Check this guide's Troubleshooting section
2. Review [QUICKSTART.md](QUICKSTART.md) for general setup issues
3. Consult PyCharm's built-in help: **Help > Find Action** and search for your issue
4. Open an issue on GitHub

---

**Happy Coding with PyCharm! 🚀**
