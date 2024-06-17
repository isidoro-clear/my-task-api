from django.db import models
from meuapp.validators import TeamInvitationValidator
from django.utils.translation import gettext_lazy as _

class TeamInvitation(models.Model):
  class Status(models.IntegerChoices):
    PENDING = 0, _('pending')
    ACCEPTED = 1, _('accepted')
    REJECTED = 2, _('rejected')

  team = models.ForeignKey('Team', on_delete=models.CASCADE, null=False)
  email = models.EmailField(null=False)
  status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

  def save(self, *args, **kwargs):
    validator = TeamInvitationValidator(self.team_id, self.email, self.status)
    validator.validate()
    super(TeamInvitation, self).save(*args, **kwargs)

  pass