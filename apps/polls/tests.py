from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.polls.models import (Profile, ProfileTest, Category,
                               Test, Answer, Question, Choice)
from apps.polls.serializers import ProfileSerializer


class AuthenticationTestCase(APITestCase):

    def test_registration(self):
        data = {'username': 'user', 'email': 'user@drfpolls.com',
                'password': 'super_strong_password'}
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_credentials_provided(self):
        username = 'user'
        password = 'super_strong_password'
        User.objects.create_user(username=username, password=password)
        data = {'username': username, 'password': password}
        access_token = self.client.post('/auth/jwt/create/', data).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer ' + access_token)
        response = self.client.get('/api/v1/polls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_credentials_not_provided(self):
        response = self.client.get('/api/v1/polls/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class JWTTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user', password='super_strong_password')

    def test_get_jwt(self):
        data = {'username': self.user.username,
                'password': 'super_strong_password'}
        response = self.client.post('/auth/jwt/create/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data and 'refresh' in response.data)


class UserProfileTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='user1', password='super_strong_password')
        self.user2 = User.objects.create_user(username='user2', password='super_strong_password')
        self.user3 = User.objects.create_user(username='user3', password='super_strong_password')

    def test_get_valid_profile(self):
        data = {'username': 'user1', 'password': 'super_strong_password'}
        access_token = self.client.post('/auth/jwt/create/', data).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer ' + access_token)
        profile = Profile.objects.get(user_id=self.user1.pk)
        response = self.client.get(reverse('polls:profile-detail', kwargs={'pk': profile.pk}))
        serializer = ProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_profile(self):
        data = {'username': 'user1', 'password': 'super_strong_password'}
        access_token = self.client.post('/auth/jwt/create/', data).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer ' + access_token)
        profile = Profile.objects.get(user=self.user2)
        response = self.client.get(reverse('polls:profile-detail', kwargs={'pk': profile.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfileTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user', password='super_strong_password')
        self.category = Category.objects.create(name='IT')
        self.test = Test.objects.create(name='Python Basics')
        self.questions = Question.objects.bulk_create([
            Question(question_text='What is a constructor in Python?',
                     test=self.test,
                     category=self.category,
                     max_points=3),
            Question(question_text='How to create an empty class?',
                     test=self.test,
                     category=self.category,
                     max_points=2)
        ])
        self.choices = Choice.objects.bulk_create([
            Choice(choice_text='__new__',
                   is_correct=False,
                   question=Question.objects.get(question_text='What is a constructor in Python?')),
            Choice(choice_text='__init__',
                   is_correct=True,
                   question=Question.objects.get(question_text='What is a constructor in Python?')),
            Choice(choice_text='__str__',
                   is_correct=False,
                   question=Question.objects.get(question_text='What is a constructor in Python?')),
            Choice(choice_text='class A: pass',
                   is_correct=True,
                   question=Question.objects.get(question_text='How to create an empty class?')),
            Choice(choice_text='class A: return',
                   is_correct=False,
                   question=Question.objects.get(question_text='How to create an empty class?')),
            Choice(choice_text='class A:',
                   is_correct=False,
                   question=Question.objects.get(question_text='How to create an empty class?')),
        ])

    def test_profile_test_mark(self):
        profile = Profile.objects.get(user_id=self.user.pk)
        answers = [
            Answer(question=Question.objects.get(question_text='What is a constructor in Python?'),
                   choice=Choice.objects.get(choice_text='__init__'),
                   user=self.user),
            Answer(question=Question.objects.get(question_text='How to create an empty class?'),
                   choice=Choice.objects.get(choice_text='class A: return'),
                   user=self.user),
        ]
        for answer in answers:
            answer.save()
        profile_test = ProfileTest.objects.get(profile=profile)
        self.assertEqual(profile_test.mark, 6.0)
