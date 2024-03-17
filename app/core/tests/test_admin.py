"""
Tests for django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Testing admin site"""
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="momo@example.com",
            password="123tesapi"
            )
        # Authenticate as Admin user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create(
            email="mimi@example.com",
            password="123MOtesting",
            name="TestUser"
        )

    def test_user_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that edit user page works."""
        # gving the path id of the user
        url = reverse('admin:core_user_change', args=(self.user.id,))
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works,"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
