from django.test import TestCase
from django.urls import reverse


class UserDashboardViewTests(TestCase):
    def test_user_dashboard_renders(self):
        response = self.client.get(reverse("dashboard:user_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cyberbullying Detection Summary")
        self.assertContains(response, "Welcome back")
