from django.db import models

class Team(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  description = models.TextField()

  def __str__(self):
    return self.name

  pass