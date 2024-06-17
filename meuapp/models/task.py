from django.db import models
from meuapp.validators import TaskValidator
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
  class Status(models.IntegerChoices):
    PENDING = 0, _('pending')
    IN_PROGRESS = 1, _('in progress')
    COMPLETED = 2, _('completed')
    CANCELED = 3, _('canceled')

  title = models.CharField(max_length=200, null=False)
  description = models.TextField(null=True)
  completed = models.BooleanField(default=False)
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

  def save(self, *args, **kwargs):
    validator = TaskValidator(self.title, self.description, self.user.id, self.status)
    validator.validate()
    super(Task, self).save(*args, **kwargs)
  
  def __str__(self):
    return self.title
  
  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "completed": self.completed,
      "user": self.user.id
    }

  pass