from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'


class Test(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Question(models.Model):
    question_text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    max_points = models.FloatField()

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ('question_text',)


class Choice(models.Model):
    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(verbose_name='is correct?')

    def __str__(self):
        return self.choice_text

    class Meta:
        ordering = ('question',)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.choice_text

    class Meta:
        ordering = ('question',)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField(Test, through='ProfileTest')

    def __str__(self):
        return str(self.user)

    @property
    def avg_test_mark(self):
        result = self.profiletest_set.filter(profile=self).aggregate(avg_mark=Avg('mark'))
        return result.get('avg_mark')

    avg_test_mark.fget.short_description = 'average test mark'

    @property
    def avg_homework_mark(self):
        result = self.homework_set.filter(profile=self).aggregate(avg_mark=Avg('mark'))
        return result.get('avg_mark')

    avg_homework_mark.fget.short_description = 'average homework mark'

    class Meta:
        ordering = ('user',)


class ProfileTest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    mark = models.FloatField(default=0)
    total_points = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_answer_count = models.IntegerField(default=0, verbose_name='correct answers')
    invalid_answer_count = models.IntegerField(default=0, verbose_name='incorrect answers')

    def __str__(self):
        return f'{self.profile.user} - {self.test.name}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'finished test'
        verbose_name_plural = 'finished tests'
