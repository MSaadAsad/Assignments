import json
import unittest
from api_project import create_app, db
from api_project.models import User

class SearchBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()
        self.jwt_token = self.get_jwt_token_for_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_jwt_token_for_test_user(self):
        response = self.client.post('/auth/login', json={
            'login_identifier': 'testuser',
            'password': 'testpassword'
        })
        token = response.get_json().get('access_token')
        return token

    def create_document(self, title, text):
        return self.client.post('/docs', json={
            'title': title,
            'text': text
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})

    def test_search_exact_match(self):
        self.create_document('Exact Match Document', 'Some text')
        response = self.client.get('api/search?q=Exact Match Document', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(any('Exact Match Document' in d['title'] for d in data['results']))

    def test_search_partial_match(self):
        self.create_document('Partial Match Document', 'Some text')
        response = self.client.get('api/search?q=Partial Match', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(any('Partial Match Document' in d['title'] for d in data['results']))

    def test_search_no_docs_in_database_no_query(self):
        response = self.client.get('api/search?q=', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')
    
    def test_search_no_docs_in_database(self):
        response = self.client.get('api/search?q=AnyText', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')
    
    def test_search_no_match_with_docs_present(self):
        self.create_document('Some Document', 'Some text')
    
        response = self.client.get('api/search?q=Nonexistent', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "No matching documents found"})

    def test_search_result_structure(self):
        self.create_document('Structure Test Document', 'Some text')
        response = self.client.get('api/search?q=Structure Test', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        for result in data['results']:
            self.assertIn('id', result)
            self.assertIn('title', result)
            self.assertIn('word_count', result)

    def test_search_special_characters(self):
        self.create_document('Special@#!$ Document', 'Some text')
        response = self.client.get('api/search?q=Special@#!$', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(any('Special@#!$ Document' in d['title'] for d in data['results']))

if __name__ == '__main__':
    unittest.main()
