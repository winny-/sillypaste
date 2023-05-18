from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


User = get_user_model()


class AuthTests(APITestCase):

    """
    Test user login/logout
    """

    # WHY CAN I NOT JUST USE A LABEL WHAT THE HECK?
    fixtures = ['api/fixtures/user_janedoe.json']

    def setUp(self):
        self.user = User.objects.get(username='janedoe')

    def inject_token(self):
        self.token = token = Token.objects.get_or_create(user=self.user)[0]
        token.save()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_login(self):
        url = reverse('api-login')
        data = {'username': 'janedoe', 'password': 'daiPh4ph'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_logout(self):
        url = reverse('api-logout')
        self.inject_token()
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'logged_out': True})
