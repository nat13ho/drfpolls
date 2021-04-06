from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from drfpolls.apps.polls import services
from drfpolls.apps.polls.models import Profile, Answer, Question, ProfileTest


@receiver(post_save, sender=User)
def auto_create_profile(sender, instance, created, **kwargs):
    """Auto creates profile when user is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Answer)
def auto_create_profile_test(sender, instance: Answer, created: bool, **kwargs):
    """Auto creates profile test when user answers all test questions."""
    if created:
        test = instance.question.test
        user_test_questions = Question.objects.filter(
            answer__user=instance.user,
            test=test)
        user_answers = services.get_answers(user=instance.user, test=test)

        if list(test.question_set.all()) == list(user_test_questions):
            ProfileTest.objects.create(
                test=test,
                profile=get_object_or_404(Profile, user=instance.user),
                mark=services.get_mark(test, user_answers),
                total_points=services.get_total_points(
                    services.get_valid_answers(user_answers)),
                valid_answer_count=services.get_valid_answer_count(user_answers),
                invalid_answer_count=services.get_invalid_answer_count(user_answers),
            )
