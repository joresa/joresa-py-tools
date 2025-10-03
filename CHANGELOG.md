# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-10-03

### Added
- Complete authentication system with secure login page
- Role-based access control (RBAC) with three user roles:
  - Admin: Full system access
  - User: Access to public and user-specific tools
  - Viewer: Basic access to public tools
- Session management using Flask-Login
- Password security with Werkzeug hashing
- Professional, responsive UI with modern styling
- Navigation menu that dynamically shows/hides based on user role
- Protected routes with role-based decorators
- Comprehensive test suite with 21 unit tests
- Demo user accounts for testing
- Complete documentation:
  - README.md with full project documentation
  - QUICKSTART.md for quick setup
  - PRODUCTION.md for production deployment guidance
- .gitignore file for Python projects

### Security Features
- Secure password hashing (Werkzeug)
- Session-based authentication (Flask-Login)
- Role-based access control decorators
- Protected routes with permission checks
- CSRF protection (Flask built-in)

### Pages Implemented
- Login page with secure authentication
- Dashboard showing role-specific information
- Public Tools page (accessible to all authenticated users)
- User Tools page (accessible to user and admin roles)
- Admin Panel (accessible to admin role only)

### Testing
- 21 comprehensive unit tests covering:
  - User authentication
  - Password hashing and verification
  - Role-based access control
  - Session management
  - Route protection
  - Permission enforcement

### Technologies Used
- Flask 3.0.0 - Web framework
- Flask-Login 0.6.3 - User session management
- Werkzeug 3.0.1 - Password hashing and security utilities
- Python 3.12+ - Programming language

[1.0.0]: https://github.com/joresa/joresa-py-tools/releases/tag/v1.0.0
