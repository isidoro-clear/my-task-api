from django.db import models

class TeamMember(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  team = models.ForeignKey('Team', on_delete=models.CASCADE)
  role = models.CharField(max_length=200, default='member')
  
  def __str__(self):
    return f'{self.user} - {self.team}'

  pass