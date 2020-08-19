import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "CA_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            'bader', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.test_post = {
            "rate": 3.5,
            "release_date": "2020-08-15T23:00:00.000Z",
            "title": "test"
        }
        self.test_bad_post = {
            "rate": 3,
            "title": "bad",

        }
        
        self.test_actor_post ={
            "name":"bader",
            "age": 26,
            "gender":"M"
        }

        self.producer = {
            'Authorization': "bearer " + os.environ['PRODUCER']

        }
        self.assistant = {
            'Authorization': "bearer " + os.environ['ASSISTANT']
        }

        self.director = {
            'Authorization': "bearer " + os.environ['DIRECTOR']
        }

        with self.app.app_context():

            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # Get endpoint test
    def test_get_movie(self):
        res = self.client().get('/movies', headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_allowed_method(self):
        res = self.client().get('/movies/1', headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    # Post endpoint test
    def test_movie_post_endpoint(self):
        res = self.client().post('/movies', json=self.test_post, headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_bad_request(self):
        res = self.client().post('/movies', json=self.test_bad_post, headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)

    def test_delete_movie(self):
        res = self.client().delete('/movies/12', headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_detete_unproccessable(self):
        res = self.client().delete('/movies/100', headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_endpoint(self):
        res = self.client().patch(
            '/movies/11',
            json={
                "title": "title test patch"},
            headers=self.producer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_assistant_unauthorized_post(self):
        res = self.client().post('/movies', json=self.test_post, headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_director_unauthorized_post(self):
        res = self.client().post('/movies', json=self.test_post, headers=self.director)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)
    
    def test_assistant_unauthorized_patch(self):
        res = self.client().patch('/movies/11',json={"title": "title test patch"}, headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 401)

    def test_director_actor_post(self):
        res = self.client().post('/actors', json=self.test_actor_post, headers=self.director)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        


if __name__ == "__main__":
    unittest.main()
