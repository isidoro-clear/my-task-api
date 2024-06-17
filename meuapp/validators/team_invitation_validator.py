from django.apps import apps

class TeamInvitationValidator:
  def __init__(self, team_id, email, status):
    self.team_id = team_id
    self.email = email
    self.status = status

  def validate(self):
    if not self.team_id:
      raise ValueError('team_id is required')
    if not self.email:
      raise ValueError('email is required')
    if not self.team_exists():
      raise ValueError('team not found')
    if self.already_invited():
      raise ValueError('user already invited to this team')
    return True
  
  def team_exists(self):
    Team = apps.get_model('meuapp', 'Team')
    try:
        Team.objects.get(id=self.team_id)
        return True
    except Team.DoesNotExist:
        return False
    
  def already_invited(self):
    TeamInvitation = apps.get_model('meuapp', 'TeamInvitation')
    try:
        TeamInvitation.objects.filter(team_id=self.team_id, email=self.email).exists()
        return True
    except TeamInvitation.DoesNotExist:
        return False