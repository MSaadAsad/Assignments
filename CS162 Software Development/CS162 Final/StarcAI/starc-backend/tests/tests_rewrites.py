import json
import unittest
from api_project import create_app, db
from api_project.models import User

class RewriteBlueprintTestCase(unittest.TestCase):

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
        response = self.client.post('/docs', json={
            'title': title,
            'text': text
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})
        return response.get_json()['document_id']

    def test_get_rewritten_sentences(self):
        document_id = self.create_document('Test Document', 'Some text')
        response = self.client.get(f'/fix/{document_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_update_sentence(self):
        document_id = self.create_document('Test Document', 'Some text')
        response = self.client.get(f'/fix/{document_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        sentences = response.get_json()
        self.assertTrue(len(sentences) > 0)
        sentence_id = sentences[0]['sentence_id']

        response = self.client.put(f'/fix/{document_id}/{sentence_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sentence and document updated successfully', response.get_data(as_text=True))

    def test_reset_sentence_to_original(self):
        document_id = self.create_document('Test Document', 'Some text')
        sentence_id = self.get_first_sentence_id(document_id)
        response = self.client.delete(f'/fix/{document_id}/{sentence_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sentence reset to original text successfully', response.get_data(as_text=True))

    def test_accept_all_suggestions(self):
        document_id = self.create_document('Test Document', 'Some text. More text. A lot of text.')
        response = self.client.put(f'/fix/{document_id}/all', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('All suggestions accepted successfully', response.get_data(as_text=True))

    def test_delete_all_suggestions(self):
        document_id = self.create_document('Test Document', 'Some text')
        response = self.client.delete(f'/fix/{document_id}/all', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('All suggestions deleted successfully', response.get_data(as_text=True))

    def get_first_sentence_id(self, document_id):
        response = self.client.get(f'/fix/{document_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        sentences = response.get_json()
        return sentences[0]['sentence_id'] if sentences else None    


if __name__ == '__main__':
    unittest.main()
