from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    def testCreateUserWithEmailSuccess(self):
        """test new user creation """
        email = "pprasha2@gmail.com"
        password = "test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def testNewUserEmailNormalized(self):
        """test that added user's email is in lower case"""
        email = "pprasha2@gmail.COM"
        password = "test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email.lower())

    def testInvalidEmail(self):
        """test if invalid email for new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def testCreateSuperUser(self):
        """test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            "pprasha2@gmail.com",
            "test123"
        )
        # built-in superuser in PermissionsMixin class
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """test the ingredient str representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='kadhai Paneer',
            time_minutes=20,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_filename_uuid(self, mock_uuid):
        """test that image is saved at correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
