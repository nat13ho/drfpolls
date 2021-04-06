from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from drfpolls.apps.polls.viewsets import CustomModelViewSet
from drfpolls.apps.tasks.serializers import HomeworkSerializer, TaskSerializer
from drfpolls.apps.tasks.models import Homework, Task


class TasksViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]


class HomeworkViewSet(CustomModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    user_actions = ['list', 'retrieve', 'partial_update']
    filterset_fields = ['homework_status']

    def get_queryset(self):
        return Homework.objects.filter(profile__user=self.request.user)
