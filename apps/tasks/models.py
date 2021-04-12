from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.polls.models import Profile


class Task(models.Model):
    task_name = models.CharField(max_length=255, verbose_name='name')
    task_text = models.TextField(verbose_name='text')

    def __str__(self):
        return self.task_name

    class Meta:
        ordering = ('task_name',)


class Homework(models.Model):
    class Status(models.TextChoices):
        RECEIVED = 'RE', _('Received')
        DONE = 'DO', _('Done')
        GRADED = 'GR', _('Graded')

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='homeworks/files/%Y/%m/%d/', null=True, blank=True)
    homework_status = models.CharField(max_length=16,
                                       choices=Status.choices,
                                       default=Status.RECEIVED)
    mark = models.FloatField(null=True, blank=True)
    mark_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.profile} - {self.task}'

    class Meta:
        ordering = ('profile', 'task')
