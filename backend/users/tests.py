from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class StaticUsersUrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Testometr')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адресов /users/ и соответсвие users:name."""
        users_pages_list = [
            ('/auth/signup/', reverse('users:signup')),
            # ('/auth/login/', reverse('users:login')),
            # ('/auth/password_reset/', reverse('users:password_reset')),
            # ('/auth/password_reset/done/',
            #  reverse('users:password_reset_done')),
            # ('/auth/password_change/', reverse('users:password_change')),
            # ('/auth/password_change/done/',
            #  reverse('users:password_change_done')),
            # ('/auth/logout/', reverse('users:logout'))
        ]

        for address, reversed_page in users_pages_list:
            with self.subTest():
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertEqual(address, reversed_page)
