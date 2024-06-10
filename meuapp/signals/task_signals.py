from django.db.models.signals import post_save
from django.dispatch import receiver
from meuapp.models import Task
from meuapp.tasks import SendRemoteNotificationTask

@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
  # if created:
  #   SendRemoteNotificationTask.send_remote_notification(instance, f'Task {instance.title} created!')

  if instance.completed:
    SendRemoteNotificationTask.send_remote_notification(instance, f'Task {instance.title} completed!')

  pass