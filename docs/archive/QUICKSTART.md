# Quick Start Guide

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize the Database
```bash
python init_db.py
```

This will:
- Create the database tables
- Seed the Diff Checker tool

### 3. Run the Application
```bash
python run.py
```

The application will start at: `http://127.0.0.1:5000`

## First Use

### Register Your Account
1. Open http://127.0.0.1:5000 in your browser
2. Click "Register" in the top right
3. Fill in your username, email, and password
4. Click "Register"

### Login
1. Use your username and password to login
2. You'll be redirected to the Dashboard

## Using the Diff Checker

### Create a Comparison
1. From the Dashboard, click on "Diff Checker" tool
2. Or navigate to Tools > Diff Checker in the menu
3. Enter your two texts in the left and right panels
4. Optionally name them (e.g., "Version 1" and "Version 2")
5. Click "Compare"

### View Diff Results
- Lines starting with `-` (red background) were removed
- Lines starting with `+` (green background) were added
- Other lines provide context

### View History
1. Click "View History" from the diff checker page
2. Or navigate to Tools > Diff History
3. Click "View" on any past comparison to see the results again

## Analytics Dashboard

### Access Analytics
1. Click "Analytics" in the main navigation
2. View three interactive charts:
   - **Most Used Tools**: Bar chart of tool popularity
   - **Usage by Date**: Line chart of daily usage
   - **Top Users**: Horizontal bar chart of most active users

## Tips

### Sample Text for Testing Diff Checker
Try comparing these two texts:

**Text 1:**
```
Hello World
This is a test
Line three
Line four
```

**Text 2:**
```
Hello World
This is a modified test
Line three
Line five
```

You should see:
- Line 2 changed (removed old, added new)
- Line 4 changed (removed "four", added "five")

## Troubleshooting

### Database Issues
If you get database errors:
```bash
rm -rf instance/
python init_db.py
```

### Port Already in Use
If port 5000 is in use, modify `run.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Missing Dependencies
If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Development Mode

The application runs in debug mode by default, which:
- Auto-reloads on code changes
- Shows detailed error pages
- Should NOT be used in production

## Production Deployment

For production:
1. Set environment variables:
   ```bash
   export SECRET_KEY='your-secure-random-key'
   export DATABASE_URL='postgresql://...'  # If using PostgreSQL
   ```

2. Disable debug mode in `run.py`:
   ```python
   app.run(debug=False)
   ```

3. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
   ```

## Next Steps

### Add More Tools
See ARCHITECTURE.md for guidance on adding new tools to the platform.

### Customize
- Modify `app/static/css/style.css` for custom styling
- Edit templates in `app/templates/` to change the UI
- Update tool descriptions in the database

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review ARCHITECTURE.md for technical details
3. Open an issue on GitHub
