from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for admin"""

    def setUp(self) -> None:
        self.Client = Client()
        self.adminUser = get_user_model().objects.create_superuser(
            email="pprasha2@gmail.com",
            password="test123"
        )
        self.Client.force_login(self.adminUser)
        self.user = get_user_model().objects.create_user(
            email="test123@gmail.com",
            password="password123",
            name="prashant"
        )

    def testUserListed(self):
        """test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.Client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def testUserChangePage(self):
        """test that user change page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.Client.get(url)
        self.assertEqual(res.status_code, 200)

    def testCreateUserPage(self):
        """test create user"""
        url = reverse('admin:core_user_add')
        res = self.Client.get(url)
        self.assertEqual(res.status_code, 200)
