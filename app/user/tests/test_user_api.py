from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREAtE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """ Test the users API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_Valid_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {
            "email": "test@mail.com",
            "password": "testpass",
            "name": "Test"
        }
        res = self.client.post(CREAtE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """ Test that user already exists """
        payload = {
            "email": "test@mail.com",
            "password": "testpass"
        }
        create_user(**payload)

        res = self.client.post(CREAtE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_to_short(self):
        """Test that password might be more than 5 characters"""
        payload = {
            'email': "test@mail.com",
            'password': "ghj"
        }

        res = self.client.post(CREAtE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']
                                                      ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for user"""
        payload = {
            'email': "some@mail.com",
            'password': "somepassword"
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not Created if invalid credentials are given"""
        create_user(email='test@mail.com', password='testpass')
        payload = {
            'email': 'testsome@mail.com',
            'password': 'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_without_user(self):
        """ Test creating token without user"""
        payload = {"email": "some@email.com", "password": "somepassword"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that password and email is required"""
        res = self.client.post(TOKEN_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
