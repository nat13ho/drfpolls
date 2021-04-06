from rest_framework import routers

from drfpolls.apps.polls import views

router = routers.DefaultRouter()
router.register(r'tests', views.TestViewSet, basename='test')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'questions', views.QuestionsViewSet, basename='question')
router.register(r'choices', views.ChoiceViewSet, basename='choice')
router.register(r'answers', views.AnswerViewSet, basename='answer')
router.register(r'profile-tests', views.ProfileTestViewSet, basename='profiletest')
router.register(r'profiles', views.ProfileViewSet, basename='profile')

app_name = 'polls'

urlpatterns = router.urls
