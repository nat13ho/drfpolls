import os

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from apps.tasks.models import Homework, Task
from apps.polls.models import Profile


@receiver(post_save, sender=Task)
def auto_create_profile_homework(sender, instance, created, **kwargs):
    """Creates user profile when user is registered."""
    if created:
        profiles = Profile.objects.all()
        homeworks = [Homework(task=instance, profile=profile) for profile in profiles]
        Homework.objects.bulk_create(homeworks)


@receiver(post_delete, sender=Homework)
def auto_delete_file_on_homework_update(sender, instance: Homework, **kwargs):
    """Deletes old homework file when corresponding homework is deleted."""
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(post_save, sender=Homework)
def auto_change_status_on_homework_update(sender, instance: Homework, created: bool, **kwargs):
    """Changes homework status on update."""
    if not created:
        graded = Homework.Status.GRADED.value
        if instance.mark and instance.homework_status != graded:
            Homework.objects.filter(pk=instance.pk).update(
                homework_status=Homework.Status.GRADED)
        elif instance.file and instance.homework_status != graded:
            Homework.objects.filter(pk=instance.pk).update(
                homework_status=Homework.Status.DONE)


@receiver(pre_save, sender=Homework)
def auto_delete_file_on_homework_update(sender, instance, **kwargs):
    """Deletes the old homework file if a new file is provided."""
    if not instance.pk:
        return False

    try:
        old_file = Homework.objects.get(pk=instance.pk).file
    except Homework.DoesNotExist:
        return False

    new_file = instance.file
    if new_file != old_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
