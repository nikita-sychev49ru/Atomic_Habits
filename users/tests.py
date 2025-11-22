from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='email_us@email.com')
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('email'), self.user.email)

    def test_users_list(self):
        url = reverse('users:user-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['email'], 'email_us@email.com')

    def test_user_register(self):
        url = reverse('users:register')
        data = {'email': 'my_example@email.com', 'password': '123*456', 'password_confirm': '123*456'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_user_register_not_valid(self):
        url = reverse('users:register')
        data = {'email': 'my_example@email.com', 'password': '123*456', 'password_confirm': '123456'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 1)

    def test_user_update(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        data = {'tg_id': '1234567890'}
        response = self.client.patch(url, data)
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('tg_id'), '1234567890')

    def test_user_delete(self):
        url = reverse('users:user-detail', args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
