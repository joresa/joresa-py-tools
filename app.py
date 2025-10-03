"""
Main Flask application with authentication system and role-based access control.
"""

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database (in production, use a real database)
users_db = {
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': generate_password_hash('admin123'),
        'role': 'admin'
    },
    'user': {
        'id': 2,
        'username': 'user',
        'password': generate_password_hash('user123'),
        'role': 'user'
    },
    'viewer': {
        'id': 3,
        'username': 'viewer',
        'password': generate_password_hash('viewer123'),
        'role': 'viewer'
    }
}


class User(UserMixin):
    """User class for Flask-Login."""
    
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role
    
    def has_role(self, role):
        """Check if user has a specific role."""
        return self.role == role
    
    def has_any_role(self, *roles):
        """Check if user has any of the specified roles."""
        return self.role in roles


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    for username, user_data in users_db.items():
        if user_data['id'] == int(user_id):
            return User(user_data['id'], username, user_data['role'])
    return None


def role_required(*roles):
    """Decorator to require specific role(s) for a route."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.has_any_role(*roles):
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def index():
    """Home page - redirects to login or dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = users_db.get(username)
        
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['id'], username, user_data['role'])
            login_user(user)
            flash(f'Welcome back, {username}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard - accessible to all authenticated users."""
    return render_template('dashboard.html', user=current_user)


@app.route('/admin')
@role_required('admin')
def admin_panel():
    """Admin panel - only accessible to admin users."""
    return render_template('admin.html', user=current_user)


@app.route('/user-tools')
@role_required('admin', 'user')
def user_tools():
    """User tools - accessible to admin and user roles."""
    return render_template('user_tools.html', user=current_user)


@app.route('/public-tools')
@login_required
def public_tools():
    """Public tools - accessible to all authenticated users."""
    return render_template('public_tools.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
