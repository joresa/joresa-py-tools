# Joresa Py Tools

A Flask-based web application with secure authentication and role-based access control.

## Features

- **Secure Authentication System**: Login page with secure password hashing
- **Role-Based Access Control (RBAC)**: Different users see different tools based on their roles
- **Session Management**: Secure session handling with Flask-Login
- **Responsive UI**: Clean, modern interface with mobile support
- **Three User Roles**:
  - **Viewer**: Basic access to dashboard and public tools
  - **User**: Access to public and user-specific tools
  - **Admin**: Full system access including admin panel

## Screenshots

### Login Page
![Login Page](https://github.com/user-attachments/assets/1a53db5e-35c6-4e67-b484-db87b3de216c)

### Admin Dashboard
![Admin Dashboard](https://github.com/user-attachments/assets/d1b14262-7ba7-4834-9e4b-06efa2aef81b)

### Admin Panel
![Admin Panel](https://github.com/user-attachments/assets/934b0e2d-f1eb-4aa1-be07-02d267ae658a)

### Viewer Dashboard (Limited Access)
![Viewer Dashboard](https://github.com/user-attachments/assets/f8c053cc-9d6c-4bd3-95c3-097640a46205)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/joresa/joresa-py-tools.git
cd joresa-py-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Demo Credentials

Use these credentials to test different role levels:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| User | user | user123 |
| Viewer | viewer | viewer123 |

## Role Permissions

### Viewer Role
- ✓ Access to Dashboard
- ✓ Access to Public Tools

### User Role
- ✓ All Viewer permissions
- ✓ Access to User Tools

### Admin Role
- ✓ All User permissions
- ✓ Access to Admin Panel
- ✓ Full system access

## Project Structure

```
joresa-py-tools/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── test_auth.py               # Authentication tests
├── app/
│   ├── templates/             # HTML templates
│   │   ├── base.html         # Base template with navigation
│   │   ├── login.html        # Login page
│   │   ├── dashboard.html    # Main dashboard
│   │   ├── admin.html        # Admin panel
│   │   ├── user_tools.html   # User tools page
│   │   └── public_tools.html # Public tools page
│   └── static/
│       └── css/
│           └── style.css     # Application styles
└── README.md
```

## Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's secure password hashing
- **Session Management**: Secure session handling with Flask-Login
- **CSRF Protection**: Flask's built-in CSRF protection
- **Role-Based Access**: Routes are protected with role-based decorators
- **Secure Redirects**: Proper redirect handling after login

## Testing

Run the test suite to verify authentication functionality:

```bash
python -m unittest test_auth.py -v
```

All 21 tests should pass, covering:
- User authentication
- Role-based access control
- Session management
- Password security
- Permission enforcement

## Development

To run in development mode:

```bash
python app.py
```

The application will start with debug mode enabled on `http://0.0.0.0:5000`

## Production Deployment

⚠️ **Important**: Before deploying to production:

1. Change the `SECRET_KEY` in `app.py` to a secure random value
2. Use a proper database instead of the in-memory mock database
3. Use a production WSGI server (e.g., Gunicorn)
4. Enable HTTPS/SSL
5. Implement proper password policies
6. Add rate limiting for login attempts
7. Set up proper logging and monitoring

## Technologies Used

- **Flask 3.0.0**: Web framework
- **Flask-Login 0.6.3**: User session management
- **Werkzeug 3.0.1**: Password hashing and security utilities
- **Python 3.12+**: Programming language

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.