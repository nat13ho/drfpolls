from apps.polls.models import (Test, Question, Answer, Choice,
                               ProfileTest, Profile, Category)
from apps.polls.serializers import (TestSerializer, QuestionSerializer,
                                    AnswerSerializer, ChoiceSerializer,
                                    ProfileTestSerializer, CategorySerializer,
                                    ProfileSerializer)
from apps.polls.viewsets import CustomModelViewSet


class TestViewSet(CustomModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_queryset(self):
        profile_tests = ProfileTest.objects.filter(profile__user=self.request.user)
        return Test.objects.exclude(profiletest__in=profile_tests)


class QuestionsViewSet(CustomModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.exclude(answer__user=self.request.user)


class AnswerViewSet(CustomModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    user_actions = ('list', 'retrieve', 'create')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)


class ChoiceViewSet(CustomModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        user_questions = Question.objects.filter(answer__user=self.request.user)
        choices = Choice.objects.exclude(question__in=user_questions)
        return choices


class CategoryViewSet(CustomModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProfileViewSet(CustomModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class ProfileTestViewSet(CustomModelViewSet):
    queryset = ProfileTest.objects.all()
    serializer_class = ProfileTestSerializer

    def get_queryset(self):
        return ProfileTest.objects.filter(profile__user=self.request.user)
