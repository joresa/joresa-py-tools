# Project Architecture

## Overview
JoResa Python Tools is a modular web application built with Flask that provides a platform for various productivity tools with user authentication and analytics.

## Architecture Layers

### 1. Application Layer (`app/`)
The application follows a modular blueprint architecture:

#### **Core Module (`app/__init__.py`)**
- Application factory pattern using `create_app()`
- Database initialization with SQLAlchemy
- Flask-Login initialization for authentication
- Blueprint registration for modular routing

#### **Database Models (`app/models.py`)**
- **User**: User accounts with password hashing
- **Tool**: Available tools in the system
- **ToolUsage**: Tracks when users use tools (for analytics)
- **DiffHistory**: Stores diff comparison history per user

### 2. Blueprint Modules

#### **Auth Blueprint (`app/auth/`)**
Handles user authentication:
- Login/Logout functionality
- User registration
- Password hashing with Werkzeug
- Session management with Flask-Login

#### **Main Blueprint (`app/main/`)**
Core application pages:
- Homepage with feature overview
- Dashboard showing available tools
- Analytics dashboard with API endpoints for charts:
  - Most used tools (last 30 days)
  - Usage by date
  - Usage by user

#### **Tools Blueprint (`app/tools/`)**
Modular tool system:
- Diff Checker: Compare two texts with highlighting
- Diff History: View past comparisons
- Tool usage tracking for analytics
- Extensible design for adding new tools

### 3. Frontend Layer

#### **Templates (`app/templates/`)**
- **Base Template**: Consistent navigation and layout
- **Bootstrap 5**: Responsive UI framework
- **Bootstrap Icons**: Iconography
- **Chart.js**: Interactive analytics charts

#### **Static Assets (`app/static/`)**
- **CSS**: Custom styling for diff output and UI enhancements
- Clean, modern design with hover effects

### 4. Configuration (`config.py`)
- Environment-based configuration
- SQLite database (easily upgradable)
- Secret key management
- Session settings

## Key Features

### Modular Tool System
New tools can be added by:
1. Creating a route in `app/tools/routes.py`
2. Creating a template
3. Adding the tool to the database
4. Tool usage is automatically tracked

### Analytics System
- Automatic tracking of tool usage
- Real-time charts showing:
  - Most popular tools
  - Usage trends over time
  - Active users
- API endpoints for data retrieval

### Authentication System
- Secure password hashing
- Session-based authentication
- Login required decorators
- User-specific data (diff history)

### Database Schema
```
users
├── id (PK)
├── username (unique)
├── email (unique)
└── password_hash

tools
├── id (PK)
├── name (unique)
├── display_name
├── description
├── icon
└── route

tool_usages
├── id (PK)
├── user_id (FK → users)
├── tool_id (FK → tools)
└── timestamp

diff_histories
├── id (PK)
├── user_id (FK → users)
├── text1_name
├── text2_name
├── text1_content
├── text2_content
├── diff_result
└── timestamp
```

## Extensibility

### Adding New Tools
The architecture is designed for easy extension:

1. **Create Route**: Add to `app/tools/routes.py`
2. **Create Form** (if needed): Add to `app/tools/forms.py`
3. **Create Template**: Add to `app/templates/tools/`
4. **Register Tool**: Add to database via `init_db.py`
5. **Track Usage**: Use `record_tool_usage()` function

### Future Enhancements
- Claims task manager
- Workflow helpers
- Document converter
- Text analyzer
- Code formatter
- File upload support
- Export functionality
- Admin panel

## Security Features
- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management
- Login required decorators
- User-specific data isolation

## Development Workflow
1. Start application: `python run.py`
2. Initialize database: `python init_db.py`
3. Access at: `http://127.0.0.1:5000`
4. Register user and explore tools

## Technology Stack
- **Backend**: Flask 3.0.0
- **Database**: SQLAlchemy ORM with SQLite
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Frontend**: Bootstrap 5, Chart.js
- **Python**: 3.8+
