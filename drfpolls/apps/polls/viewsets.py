from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    """ModelViewSet with user action permissions."""
    user_actions = ['list', 'retrieve']

    def get_permissions(self):
        if self.action in self.user_actions:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
