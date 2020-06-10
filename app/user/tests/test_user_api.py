from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**param):
    return get_user_model().objects.create_user(**param)


class PublicApiTests(TestCase):
    """tests the user API public"""

    def setUp(self):
        self.client = APIClient()

    def test_valid_user_success(self):
        """test creating a user"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "test123",
            "name": "prashant"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """create an existing user again"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "test123",
            "name": "prashant"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """password must be more than 5 characters"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "test",
            "name": "prashant"
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """test that token is created for user"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "test123",
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """test that token is not created when invalid credentials are given"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "test123",
        }
        payload_invalid = {
            "email": "pprasha2@gmail.com",
            "password": "test1234",
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload_invalid)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test token is not created when user is not present"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "test123",
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test that email and password are required"""
        payload = {
            "email": "pprasha2@gmail.com",
            "password": "",
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorised(self):
        """test that authentication is required for user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """test API requests that require authentication"""

    def setUp(self):
        """setup tests"""
        self.user = create_user(
            email='pprasha2@yopmailll.com',
            password='test1234',
            name='prashant'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_no_post_allowed(self):
        """test that post is not allowed"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating user profile for authenticated user"""
        payload = {
            'name': 'new_name',
            'password': 'newpassword'
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
