import unittest
from api_project import create_app, db
from api_project.models import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        user1 = User(username='testuser', email='test@example.com')
        user1.set_password('testpassword')
        user2 = User(username='anotheruser', email='another@example.com')
        user2.set_password('anotherpassword')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user_success(self):
        response = self.client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Registered successfully', response.get_data(as_text=True))

    def test_register_user_with_existing_username(self):
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'email': 'unique@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', response.get_data(as_text=True))

    def test_register_user_with_existing_email(self):
        response = self.client.post('/auth/register', json={
            'username': 'uniqueuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email already registered', response.get_data(as_text=True))

    def test_register_user_missing_fields(self):
        response = self.client.post('/auth/register', json={
            'username': 'user'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username, email, and password required', response.get_data(as_text=True))

    def login_user_helper(self, identifier, password):
        return self.client.post('/auth/login', json={
            'login_identifier': identifier,
            'password': password
        })

    def test_login_user_with_username_success(self):
        response = self.login_user_helper('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_login_user_with_email_success(self):
        response = self.login_user_helper('test@example.com', 'testpassword')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_login_user_with_invalid_credentials(self):
        response = self.login_user_helper('testuser', 'wrongpassword')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.get_data(as_text=True))

    def login_and_get_token(self, username, password):
        response = self.client.post('/auth/login', json={
            'login_identifier': username,
            'password': password
        })
        return response.get_json().get('access_token')

    def test_logout_user(self):
        token = self.login_and_get_token('testuser', 'testpassword')

        response = self.client.post('/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access token has been revoked', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
