from django.db import models
from meuapp.validators import TeamMemberValidator

class TeamMember(models.Model):
  user = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
  team = models.ForeignKey('Team', on_delete=models.CASCADE, null=False)
  role = models.CharField(max_length=200, default='member')

  def save(self, *args, **kwargs):
    validator = TeamMemberValidator(self.team_id, self.user_id, self.role)
    validator.validate()
    super(TeamMember, self).save(*args, **kwargs)
  
  def __str__(self):
    return f'{self.user} - {self.team}'

  pass