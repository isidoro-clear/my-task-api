from django.db import models
from meuapp.validators import TeamValidator

class Team(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  description = models.TextField()

  def save(self, *args, **kwargs):
    validator = TeamValidator(self.user_id, self.name, self.description)
    validator.validate()
    super(Team, self).save(*args, **kwargs)

  def __str__(self):
    return self.name

  pass