from django.db.models.signals import post_save
from django.dispatch import receiver
from dotenv import dotenv_values
from meuapp.models import TeamInvitation, User, TeamMember
from meuapp.tasks import SendRemoteNotificationTask

@receiver(post_save, sender=TeamInvitation)
def team_invitation_post_save(sender, instance, created, **kwargs):
  if created:
    env_values = dotenv_values('.env')
    SendRemoteNotificationTask.send_remote_notification(instance, f'Team invitation for {instance.email} created!', payload={'link': f'{env_values["BASE_URL"]}/team_invitations/{instance.id}/accept'})
  
  if instance.status == 'accepted':
    user = User.objects.create(first_name=instance.email.split('@')[0], last_name='', email=instance.email, password='123456')
    TeamMember.objects.create(team=instance.team, user=user)
    SendRemoteNotificationTask.send_remote_notification(instance, f'You have been added to the team {instance.team.name}!\nAccess Password: {user.password}')
  pass