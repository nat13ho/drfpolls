from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/v1/polls/', include('drfpolls.apps.polls.urls', namespace='polls')),
    path('api/v1/tasks/', include('drfpolls.apps.tasks.urls', namespace='tasks')),
]
