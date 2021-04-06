from django.contrib.auth.models import User
from django.db.models import QuerySet, Sum

from drfpolls.apps.polls.models import Test, Answer, Question


def get_answers(user: User, test: Test) -> QuerySet[Answer]:
    """Returns user answers of a given test."""
    answers = Answer.objects.filter(
        user=user,
        choice__question__test=test
    )
    return answers


def get_mark(test: Test, answers: QuerySet[Answer]) -> float:
    """Calculates and returns grade of a given test."""
    valid_answers = get_valid_answers(answers)
    total_points = get_total_points(valid_answers)
    max_points = get_max_points(test)
    mark = total_points * 10 / max_points
    return mark


def get_valid_answer_count(answers: QuerySet[Answer]) -> int:
    """Returns count of valid answers"""
    return answers.filter(choice__is_correct=True).count()


def get_invalid_answer_count(answers: QuerySet[Answer]) -> int:
    """Returns count of invalid answers"""
    return answers.filter(choice__is_correct=False).count()


def get_valid_answers(answers: QuerySet[Answer]) -> QuerySet[Answer]:
    return answers.filter(choice__is_correct=True)


def get_total_points(valid_answers: QuerySet[Answer]) -> float:
    """Returns user test points"""
    return valid_answers.aggregate(
        total_points=Sum('question__max_points')
    )['total_points']


def get_max_points(test: Test) -> float:
    """Returns max test points"""
    return Question.objects.filter(
        test=test
    ).aggregate(max_points=Sum('max_points'))['max_points']
