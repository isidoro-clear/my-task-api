from django.db import models

class TeamInvitation(models.Model):
  team = models.ForeignKey('Team', on_delete=models.CASCADE)
  email = models.EmailField()
  status = models.CharField(max_length=20, default='pending')

  pass