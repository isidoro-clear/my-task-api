from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from meuapp.models import Task
from meuapp.tasks import SendRemoteNotificationTask
from meuapp.services import ElasticsearchService



@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
  if created:
    elasticsearch = ElasticsearchService()
    elasticsearch.index(index="tasks", id=instance.id, body=instance.to_dict())
  else:
    elasticsearch = ElasticsearchService()
    elasticsearch.update(index="tasks", id=instance.id, body=instance.to_dict())

  if instance.completed:
    SendRemoteNotificationTask.send_remote_notification(instance, f'Task {instance.title} completed!')

  pass

@receiver(post_delete, sender=Task)
def task_post_delete(sender, instance, **kwargs):
  elasticsearch = ElasticsearchService()
  elasticsearch.delete(index="tasks", id=instance.id)
  pass