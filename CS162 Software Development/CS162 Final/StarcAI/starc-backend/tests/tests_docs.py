import unittest
from api_project import create_app, db
from api_project.models import User, Document
from api_project.routes.documents import process_document

class DocumentBlueprintTestCase(unittest.TestCase):

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
        self.test_user_id = test_user.id
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

    def test_create_document_success(self):
        response = self.client.post('/docs', json={
            'title': 'Test Title',
            'text': 'Test Text.'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Document and text chunk processed successfully', response.get_data(as_text=True))

    def test_create_document_missing_title(self):
        response = self.client.post('/docs', json={
            'text': 'Test Text'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Title and text are required', response.get_data(as_text=True))

    def test_delete_document_success(self):
        document = Document(title='Test Document', user_id=self.test_user_id)
        db.session.add(document)
        db.session.commit()

        response = self.client.delete(f'/docs/{document.id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Document and related data deleted successfully', response.get_data(as_text=True))

    def test_create_document_unauthorized(self):
        response = self.client.post('/docs', json={
            'title': 'Test Title',
            'text': 'Test Text'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', response.get_data(as_text=True))

    def test_update_title_success(self):
        post_response = self.client.post('/docs', json={
            'title': 'Test Document',
            'text': 'New Text'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})

        post_data = post_response.get_json()
        document_id = post_data['document_id']

        put_response = self.client.put(f'/docs/{document_id}', json={
            'title': 'Title',
            'text': 'New Text'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})
        
        self.assertEqual(put_response.status_code, 200)
        self.assertIn('Title updated successfully', put_response.get_data(as_text=True))

    def test_update_text_success(self):
        post_response = self.client.post('/docs', json={
            'title': 'Test Document',
            'text': 'New Text'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})

        post_data = post_response.get_json()
        document_id = post_data['document_id']

        put_response = self.client.put(f'/docs/{document_id}', json={
            'title': 'Test Document',
            'text': '''Never gonna give you up
            Never gonna let you down
            Never gonna run around and desert you
            Never gonna make you cry
            Never gonna say goodbye
            Never gonna tell a lie and hurt you
            '''
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})
        
        self.assertEqual(put_response.status_code, 200)
        self.assertIn('Text updated successfully', put_response.get_data(as_text=True))

    def test_get_original_scores_success(self):
        response = self.client.post('/docs', json={
            'title': 'Test Document',
            'text': 'Jumps and jumps the jumps over lazy a fox the. Fox lazy quick a runs fox dog into the lazy. And jumps quick the brown the and runs lazy field. Fox over lazy runs a into lazy field field jumps. Quick the runs jumps field into jumps jumps and a.'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        document_id = json_data['document_id']
        
        response = self.client.get(f'/docs/scores/{document_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)

        scores_data = response.get_json()
        self.assertIsInstance(scores_data, list)
        self.assertGreater(len(scores_data), 0)
        for score in scores_data:
            self.assertIn('score', score)
            self.assertIn('optimism', score)
            self.assertIn('forecast', score)
            self.assertIn('confidence', score)

    def test_get_document_details_success(self):
        response = self.client.post('/docs', json={
            'title': 'Test Document',
            'text': 'Sample text for document details test.'
        }, headers={'Authorization': f'Bearer {self.jwt_token}'})

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        document_id = json_data['document_id']

        response = self.client.get(f'/docs/{document_id}', headers={'Authorization': f'Bearer {self.jwt_token}'})
        self.assertEqual(response.status_code, 200)
        
        details_data = response.get_json()
        self.assertEqual(details_data['title'], 'Test Document')
        self.assertTrue('word_count' in details_data)
        self.assertIsInstance(details_data['sentences_combined'], str)

if __name__ == '__main__':
    unittest.main()
