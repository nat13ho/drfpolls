from rest_framework import routers

from apps.tasks.views import TasksViewSet, HomeworkViewSet

app_name = 'tasks'

router = routers.DefaultRouter()
router.register(r'tasks', TasksViewSet)
router.register(r'homeworks', HomeworkViewSet)

urlpatterns = router.urls
