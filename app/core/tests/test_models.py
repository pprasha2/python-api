from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def testCreateUserWithEmailSuccess(self):
        """test new user creation """
        email = "pprasha2@gmail.com"
        password = "test123"
        user = get_user_model().objects.CreateUser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def testNewUserEmailNormalized(self):
        """test that added user's email is in lower case"""
        email = "pprasha2@gmail.COM"
        password = "test123"
        user = get_user_model().objects.CreateUser(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def testInvalidEmail(self):
        """test if invalid email for new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.CreateUser(None, "test123")

    def testCreateSuperUser(self):
        """test creating a superuser"""
        user = get_user_model().objects.CreateSuperUser(
            "pprasha2@gmail.com",
            "test123"
        )
        # built-in superuser in PermissionsMixin class
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
