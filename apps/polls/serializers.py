from django.shortcuts import get_object_or_404

from rest_framework import serializers

from apps.polls.models import (Test, Question, Answer,
                               Choice, ProfileTest, Profile,
                               Category)


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    question = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Choice
        fields = ('url', 'id', 'choice_text', 'question')
        extra_kwargs = {
            'url': {'view_name': 'polls:choice-detail'},
        }


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    choices = ChoiceSerializer(source='choice_set.all', many=True, read_only=True)
    test = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ('url', 'id', 'question_text',
                  'category', 'test', 'max_points', 'choices')
        extra_kwargs = {
            'url': {'view_name': 'polls:question-detail'},
        }


class TestSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(source='question_set.all', many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('url', 'id', 'name', 'questions')
        extra_kwargs = {
            'url': {'view_name': 'polls:test-detail'},
        }


class AnswerSerializer(serializers.ModelSerializer):
    choice = serializers.StringRelatedField(read_only=True)
    question = serializers.StringRelatedField(read_only=True)

    def validate_choice(self, choice):
        question: Question = get_object_or_404(
            Question,
            pk=int(self.initial_data.get('question'))
        )
        if not question.choices.filter(choice=choice).exists():
            raise serializers.ValidationError('There is no given answer choice for this question.')
        return choice

    def validate_question(self, question):
        request = self.context.get('request')
        if request and Answer.objects.filter(
                question=question,
                user=request.user).exists():
            raise serializers.ValidationError('You have already answered this question.')
        return question

    class Meta:
        model = Answer
        fields = ('id', 'choice', 'question', 'created_at')


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'avg_test_mark', 'avg_homework_mark')

    def get_username(self, profile: Profile):
        return profile.user.username


class ProfileTestSerializer(serializers.ModelSerializer):
    test = serializers.StringRelatedField(read_only=True)

    def validate_test(self, test):
        if not Test.objects.filter(test=test).exists():
            raise serializers.ValidationError('There is no test with given primary key.')
        elif ProfileTest.objects.filter(
                profile__user=self.context.get('request').user,
                test=test).exists():
            raise serializers.ValidationError('You have already finished this test.')
        return test

    class Meta:
        model = ProfileTest
        fields = ('id', 'test', 'mark',
                  'total_points', 'valid_answer_count',
                  'invalid_answer_count', 'created_at')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('url', 'id', 'name')
        extra_kwargs = {
            'url': {'view_name': 'polls:category-detail'},
        }