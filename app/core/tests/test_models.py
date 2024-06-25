"""
Tests for models
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


class ModelTests(TestCase):
    def test_create_user_with_email_password(self):
        """Test creating a user with an email is successful"""
        email = 'momo@example.com'
        password = '123testpass'
        user = get_user_model().objects.create_user(
            email='momo@example.com',
            password='123testpass',
            )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Testing that the emails are normalized"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
        ]

        for given, expected in sample_emails:
            user = get_user_model().objects.create_user(email=given)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '123test')

    def test_create_superuser(self):
        """Test creating a superuser"""
        super_user = get_user_model().objects.create_superuser(
            "test1@example.com",
            "123testing",
        )
        self.assertEqual(super_user.email, "test1@example.com")
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            name="Mohamed",
            email="Test@example.com",
            password="testpass123"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample title',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample recipe description.'
        )
        self.assertEqual(str(recipe), recipe.title)
