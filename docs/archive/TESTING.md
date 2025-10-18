# Testing Guide

This document describes how to test the JoResa Python Tools application.

## Manual Testing Checklist

### Authentication
- [ ] Register new user with valid data
- [ ] Register with invalid email - should show error
- [ ] Register with existing username - should show error
- [ ] Login with correct credentials
- [ ] Login with incorrect password - should show error
- [ ] Login with non-existent user - should show error
- [ ] Test "Remember Me" functionality
- [ ] Logout successfully
- [ ] Try accessing protected route without login - should redirect to login

### Dashboard
- [ ] Dashboard loads successfully after login
- [ ] All available tools are displayed
- [ ] Tool cards have correct icons and descriptions
- [ ] Recent activity shows up (after using tools)
- [ ] Navigation menu works correctly

### Diff Checker Tool
- [ ] Access diff checker from dashboard
- [ ] Access diff checker from Tools menu
- [ ] Compare two simple texts
- [ ] Compare texts with special characters
- [ ] Compare texts with line breaks
- [ ] Compare identical texts
- [ ] Compare with empty text - should show validation error
- [ ] Verify red highlighting for removed lines
- [ ] Verify green highlighting for added lines
- [ ] Custom names for Text 1 and Text 2
- [ ] Click "View History" button

### Diff History
- [ ] History page shows all past comparisons
- [ ] History is sorted by date (newest first)
- [ ] Click "View" to see specific comparison
- [ ] Verify original texts are preserved
- [ ] Verify diff result is preserved
- [ ] History is user-specific (other users can't see it)

### Analytics Dashboard
- [ ] Analytics page loads successfully
- [ ] "Most Used Tools" chart displays
- [ ] "Usage by Date" chart displays
- [ ] "Usage by User" chart displays
- [ ] Charts update after tool usage
- [ ] Hover over charts shows tooltips
- [ ] Charts are responsive on mobile

### UI/UX
- [ ] All pages have consistent header/footer
- [ ] Navigation menu highlights current page
- [ ] Flash messages appear and are dismissible
- [ ] Forms have proper validation
- [ ] Error messages are clear and helpful
- [ ] Success messages are visible
- [ ] Page titles are correct
- [ ] Favicon loads (if added)

### Responsive Design
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768x1024)
- [ ] Test on mobile (375x667)
- [ ] Navigation collapses on mobile
- [ ] Forms are usable on mobile
- [ ] Charts are readable on small screens

### Security
- [ ] Cannot access /dashboard without login
- [ ] Cannot access /tools/* without login
- [ ] Cannot access /analytics without login
- [ ] Cannot view other users' diff history
- [ ] CSRF token is present in forms
- [ ] Passwords are hashed in database
- [ ] SQL injection attempts fail

### Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## Automated Testing (Future)

Example test structure for unit tests:

```python
# tests/test_auth.py
import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register(self):
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        # Create user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Test login
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## Performance Testing

Test with multiple users:
- Create 100+ users
- Generate 1000+ tool usage entries
- Check analytics page load time
- Check dashboard responsiveness
- Monitor database query performance

## Database Testing

```bash
# Create test database
python init_db.py

# Add test data
python
>>> from app import create_app, db
>>> from app.models import User, Tool, ToolUsage
>>> app = create_app()
>>> with app.app_context():
...     # Create 10 test users
...     for i in range(10):
...         user = User(username=f'user{i}', email=f'user{i}@test.com')
...         user.set_password('password')
...         db.session.add(user)
...     db.session.commit()
```

## Test Data

### Sample texts for diff testing:

**Text 1:**
```
The quick brown fox
jumps over the lazy dog.
This is line three.
This is line four.
```

**Text 2:**
```
The quick brown fox
leaps over the lazy dog.
This is line three.
This is line five.
```

**Expected result:**
- Line 2 changed (jumps → leaps)
- Line 4 changed (four → five)

## Stress Testing

Test with:
- Very long texts (10,000+ characters)
- Texts with many differences
- Rapid successive comparisons
- Multiple concurrent users

## Bug Tracking

When you find a bug:
1. Document it clearly
2. Create a GitHub issue
3. Include reproduction steps
4. Add screenshots if relevant
5. Note the environment

## Testing Checklist Before Release

- [ ] All manual tests pass
- [ ] No console errors
- [ ] No broken links
- [ ] All forms work correctly
- [ ] Database migrations tested
- [ ] Documentation is up to date
- [ ] README instructions work
- [ ] Requirements.txt is complete
- [ ] .gitignore is correct
- [ ] No sensitive data in repo

## Future Improvements

- Add unit tests with pytest
- Add integration tests
- Set up CI/CD with GitHub Actions
- Add code coverage reporting
- Implement end-to-end tests with Selenium
- Add performance benchmarks
