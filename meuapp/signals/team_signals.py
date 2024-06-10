from django.db.models.signals import post_save
from django.dispatch import receiver
from meuapp.models import Team, TeamMember

@receiver(post_save, sender=Team)
def team_post_save(sender, instance, created, **kwargs):
  if created:
    TeamMember.objects.create(user=instance.user, team=instance, role='admin')
  pass