from django.urls import reverse
from rest_framework.test import APITestCase,URLPatternsTestCase
from rest_framework import status
# Create your tests here.

class LoginEndpointTest(APITestCase):
    def test_create_account(self):
        url=reverse('user_login')
        response = self.client.post(url, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
