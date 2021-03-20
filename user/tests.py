# /api/tests.py

from django.test import TestCase
from .models import User
from rest_framework import status
import json

class ModelTestCase(TestCase):
    def testCreate(self):
        old_count = User.objects.count()
        data = {"name": "john1", "password": "a", "firstName": "john", "middleName": "a","lastName": "smith", "email": "test@gmail.com", "telephone": "11144441111"}
        response = self.client.post('/user/create/', data, format='json')
        new_count = User.objects.count()
        self.assertNotEqual(old_count, new_count)

    def testGet(self):
        data = {"name": "john2", "password": "a", "firstName": "john", "middleName": "a","lastName": "smith", "email": "test@gmail.com", "telephone": "11144441111"}
        response = self.client.post('/user/create/', data, format='json')
        response = self.client.get('/user/' + str(json.loads(response.content)['id']) + '/')
        self.assertEqual(json.loads(response.content)['name'], "john2")

    def testGetAll(self):
        data = {"name": "john3", "password": "a", "firstName": "john", "middleName": "a","lastName": "smith", "email": "test@gmail.com", "telephone": "11144441111"}
        response1 = self.client.post('/user/create/', data, format='json')
        data['name'] = 'john4'
        response2 = self.client.post('/user/create/', data, format='json')
        data['name'] = 'john5'
        response3 = self.client.post('/user/create/', data, format='json')
        response = self.client.get('/user/')
        self.assertEqual(json.loads(response.content)[0]['name'], "john3")
        self.assertEqual(json.loads(response.content)[1]['name'], "john4")
        self.assertEqual(json.loads(response.content)[2]['name'], "john5")

    def testUpdate(self):
        data = {"name": "john6", "password": "a", "firstName": "john", "middleName": "a","lastName": "smith", "email": "test@gmail.com", "telephone": "11144441111"}
        response = self.client.post('/user/create/', data, format='json')
        data['name'] = 'joe'
        response = self.client.put('/user/update/' + str(json.loads(response.content)['id']) + '/', data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/user/' + str(json.loads(response.content)['id']) + '/')
        self.assertEqual(json.loads(response.content)['name'], "joe")

    def testDelete(self):
        data = {"name": "john7", "password": "a", "firstName": "john", "middleName": "a","lastName": "smith", "email": "test@gmail.com", "telephone": "11144441111"}
        response = self.client.post('/user/create/', data, format='json')
        response = self.client.get('/user/' + str(json.loads(response.content)['id']) + '/')
        self.assertEqual(json.loads(response.content)['name'], "john7")
        response = self.client.delete('/user/delete/' + str(json.loads(response.content)['id']) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
