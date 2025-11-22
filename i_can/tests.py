from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

from .models import Habit


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='email_us@email.com')
        self.pleasant_habit = Habit.objects.create(action='почитать роман', user=self.user, is_pleasant=True)
        self.good_habit = Habit.objects.create(
            action='выучить 5 английских слов',
            user=self.user,
            periodicity=1,
            start_time='19:50:00',
            related_habit=self.pleasant_habit,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse('i_can:habit', args=(self.good_habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), self.good_habit.action)

    def test_habit_list(self):
        url = reverse('i_can:habits')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'][0]['action'], 'выучить 5 английских слов')

    def test_public_habit_list(self):
        url = reverse('i_can:public')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['results'], [])

    def test_habit_create(self):
        url = reverse('i_can:habit_create')
        data = {
            "action": "сделать 20 приседаний",
            "place": "дома",
            "periodicity": 1,
            "is_pleasant": False,
            "execution_time": 90,
            "start_time": "06:50:00",
            "reward": "йогурт",
            "is_published": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)

    def test_habit_create_not_valid1(self):
        url = reverse('i_can:habit_create')
        data = {
            "action": "сделать 20 приседаний",
            "place": "дома",
            "periodicity": 10,
            "is_pleasant": False,
            "execution_time": 90,
            "start_time": "06:50:00",
            "reward": "йогурт",
            "is_published": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_not_valid2(self):
        url = reverse('i_can:habit_create')
        data = {
            "action": "сделать 20 приседаний",
            "place": "дома",
            "periodicity": 7,
            "is_pleasant": True,
            "execution_time": 90,
            "start_time": "06:50:00",
            "reward": "йогурт",
            "is_published": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_not_valid3(self):
        url = reverse('i_can:habit_create')
        data = {
            "action": "сделать 20 приседаний",
            "place": "дома",
            "periodicity": 7,
            "is_pleasant": False,
            "execution_time": 200,
            "start_time": "06:50:00",
            "reward": "йогурт",
            "is_published": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_not_valid4(self):
        url = reverse('i_can:habit_create')
        data = {
            "action": "сделать 20 приседаний",
            "place": "дома",
            "periodicity": 7,
            "is_pleasant": False,
            "execution_time": 100,
            "start_time": "06:50:00",
            "reward": "йогурт",
            "related_habit": 1,
            "is_published": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse('i_can:habit_update', args=(self.good_habit.pk,))
        data = {"start_time": "06:50:00", "action": "сделать 20 приседаний"}
        response = self.client.patch(url, data, format='json')
        result = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get('action'), 'сделать 20 приседаний')

    def test_habit_delete(self):
        url = reverse('i_can:habit_delete', args=(self.good_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)
