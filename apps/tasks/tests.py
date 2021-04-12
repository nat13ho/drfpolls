from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.polls.models import Profile
from apps.tasks.models import Homework, Task
from apps.tasks.serializers import HomeworkSerializer


class HomeworkTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user', password='super_strong_password')
        self.profile = Profile.objects.get(user_id=self.user.pk)
        self.tasks = Task.objects.bulk_create([
            Task(task_name='Task 1', task_text='Task 1'),
            Task(task_name='Task 2', task_text='Task 2'),
            Task(task_name='Task 3', task_text='Task 3'),
            Task(task_name='Task 4', task_text='Task 4')
        ])
        self.homeworks = Homework.objects.bulk_create([
            Homework(task=Task.objects.get(task_name='Task 1'),
                     homework_status=Homework.Status.GRADED,
                     profile=self.profile,
                     mark=7.0),
            Homework(task=Task.objects.get(task_name='Task 2'),
                     homework_status=Homework.Status.DONE,
                     profile=self.profile),
            Homework(task=Task.objects.get(task_name='Task 3'),
                     homework_status=Homework.Status.RECEIVED,
                     profile=self.profile),
            Homework(task=Task.objects.get(task_name='Task 4'),
                     homework_status=Homework.Status.RECEIVED,
                     profile=self.profile),
        ])
        access_token = self.client.post('/auth/jwt/create/', data={
            'username': self.user.username,
            'password': 'super_strong_password'
        }).data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer ' + access_token)

    def test_get_received_homework(self):
        homeworks = Homework.objects.filter(homework_status=Homework.Status.RECEIVED)
        serializer = HomeworkSerializer(homeworks, many=True)
        response = self.client.get(reverse('tasks:homework-list') + '?homework_status=RE')
        self.assertEqual(serializer.data, response.data)

    def test_get_done_homework(self):
        homeworks = Homework.objects.filter(homework_status=Homework.Status.DONE)
        serializer = HomeworkSerializer(homeworks, many=True)
        response = self.client.get(reverse('tasks:homework-list') + '?homework_status=DO')
        self.assertEqual(serializer.data, response.data)

    def test_get_graded_homework(self):
        homeworks = Homework.objects.filter(homework_status=Homework.Status.GRADED)
        serializer = HomeworkSerializer(homeworks, many=True)
        response = self.client.get(reverse('tasks:homework-list') + '?homework_status=GR')
        self.assertEqual(serializer.data, response.data)



