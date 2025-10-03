"""
Tests for the authentication system.
"""

import unittest
from app import app, User, users_db, role_required
from werkzeug.security import check_password_hash


class AuthenticationTestCase(unittest.TestCase):
    """Test cases for authentication system."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
    
    def test_users_database_exists(self):
        """Test that users database is properly configured."""
        self.assertIn('admin', users_db)
        self.assertIn('user', users_db)
        self.assertIn('viewer', users_db)
    
    def test_user_passwords_are_hashed(self):
        """Test that passwords are stored as hashes."""
        for username, user_data in users_db.items():
            # Password should be hashed, not plain text
            self.assertNotEqual(user_data['password'], 'admin123')
            self.assertNotEqual(user_data['password'], 'user123')
            self.assertNotEqual(user_data['password'], 'viewer123')
    
    def test_password_verification(self):
        """Test password hash verification."""
        admin_data = users_db['admin']
        self.assertTrue(check_password_hash(admin_data['password'], 'admin123'))
        self.assertFalse(check_password_hash(admin_data['password'], 'wrongpassword'))
    
    def test_user_roles(self):
        """Test that users have correct roles assigned."""
        self.assertEqual(users_db['admin']['role'], 'admin')
        self.assertEqual(users_db['user']['role'], 'user')
        self.assertEqual(users_db['viewer']['role'], 'viewer')
    
    def test_user_class_has_role_method(self):
        """Test User class has_role method."""
        admin_user = User(1, 'admin', 'admin')
        self.assertTrue(admin_user.has_role('admin'))
        self.assertFalse(admin_user.has_role('user'))
    
    def test_user_class_has_any_role_method(self):
        """Test User class has_any_role method."""
        user_user = User(2, 'user', 'user')
        self.assertTrue(user_user.has_any_role('admin', 'user'))
        self.assertTrue(user_user.has_any_role('user'))
        self.assertFalse(user_user.has_any_role('admin', 'viewer'))
    
    def test_login_page_loads(self):
        """Test that login page is accessible."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)
    
    def test_index_redirects_to_login(self):
        """Test that index redirects to login for unauthenticated users."""
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_successful_login(self):
        """Test successful login with valid credentials."""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)
    
    def test_failed_login_wrong_password(self):
        """Test login failure with wrong password."""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_failed_login_wrong_username(self):
        """Test login failure with non-existent username."""
        response = self.client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_dashboard_requires_authentication(self):
        """Test that dashboard requires login."""
        response = self.client.get('/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_admin_panel_requires_authentication(self):
        """Test that admin panel requires login."""
        response = self.client.get('/admin', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_user_tools_requires_authentication(self):
        """Test that user tools require login."""
        response = self.client.get('/user-tools', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_authenticated_user_can_access_dashboard(self):
        """Test that authenticated user can access dashboard."""
        with self.client:
            self.client.post('/login', data={
                'username': 'viewer',
                'password': 'viewer123'
            })
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Dashboard', response.data)
    
    def test_viewer_cannot_access_admin_panel(self):
        """Test that viewer role cannot access admin panel."""
        with self.client:
            self.client.post('/login', data={
                'username': 'viewer',
                'password': 'viewer123'
            })
            response = self.client.get('/admin', follow_redirects=True)
            self.assertIn(b'do not have permission', response.data)
    
    def test_viewer_cannot_access_user_tools(self):
        """Test that viewer role cannot access user tools."""
        with self.client:
            self.client.post('/login', data={
                'username': 'viewer',
                'password': 'viewer123'
            })
            response = self.client.get('/user-tools', follow_redirects=True)
            self.assertIn(b'do not have permission', response.data)
    
    def test_user_can_access_user_tools(self):
        """Test that user role can access user tools."""
        with self.client:
            self.client.post('/login', data={
                'username': 'user',
                'password': 'user123'
            })
            response = self.client.get('/user-tools')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User Tools', response.data)
    
    def test_user_cannot_access_admin_panel(self):
        """Test that user role cannot access admin panel."""
        with self.client:
            self.client.post('/login', data={
                'username': 'user',
                'password': 'user123'
            })
            response = self.client.get('/admin', follow_redirects=True)
            self.assertIn(b'do not have permission', response.data)
    
    def test_admin_can_access_all_pages(self):
        """Test that admin role can access all pages."""
        with self.client:
            self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            
            response = self.client.get('/user-tools')
            self.assertEqual(response.status_code, 200)
            
            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 200)
    
    def test_logout_works(self):
        """Test that logout functionality works."""
        with self.client:
            self.client.post('/login', data={
                'username': 'admin',
                'password': 'admin123'
            })
            
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'logged out successfully', response.data)
            
            # After logout, should not be able to access protected pages
            response = self.client.get('/dashboard', follow_redirects=False)
            self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
