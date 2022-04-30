from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@mail.com', password='testpass'):
    """Create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_email_successfully(self):
        """ Test new user Creation with email and password is successful """
        email = 'test@londonappdev.com'
        password = 'testwordpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
                                                    )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """ Test the email for a new user, is normalized """
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email=email,
                                                    password='Random4')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test Creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating new superuser """
        user = get_user_model().objects.create_superuser(
            email='test@test.com',
            password='random4'
                                                         )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test ingredient string representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
