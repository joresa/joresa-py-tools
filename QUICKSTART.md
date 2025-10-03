# Quick Start Guide

## Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python app.py
```

### 3. Open in Browser
Navigate to: `http://localhost:5000`

## Login with Demo Accounts

### Admin Account (Full Access)
- Username: `admin`
- Password: `admin123`
- Access: Dashboard, Public Tools, User Tools, Admin Panel

### User Account (Standard Access)
- Username: `user`
- Password: `user123`
- Access: Dashboard, Public Tools, User Tools

### Viewer Account (Limited Access)
- Username: `viewer`
- Password: `viewer123`
- Access: Dashboard, Public Tools

## What to Try

1. **Login as Admin** - See all features and navigation options
2. **Visit Admin Panel** - Only accessible to admin role
3. **Logout and Login as Viewer** - Notice the limited navigation menu
4. **Try accessing protected routes** - See role-based access control in action

## Running Tests

Verify everything works:
```bash
python -m unittest test_auth.py -v
```

All 21 tests should pass.

## Troubleshooting

**Port 5000 already in use?**
Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

**Dependencies not installing?**
Make sure you have Python 3.8+ installed:
```bash
python --version
```

## Next Steps

- Change the `SECRET_KEY` in `app.py` for production
- Replace the mock database with a real database (SQLite, PostgreSQL, etc.)
- Add more tools and features specific to your needs
- Customize the UI colors and branding
- Set up HTTPS for secure production deployment
