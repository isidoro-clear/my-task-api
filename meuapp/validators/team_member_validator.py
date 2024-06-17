from django.apps import apps

class TeamMemberValidator:
  def __init__(self, team_id, user_id, role):
    self.team_id = team_id
    self.user_id = user_id
    self.role = role

  def validate(self):
    if not self.team_id:
      raise ValueError('team_id is required')
    if not self.user_id:
      raise ValueError('user_id is required')
    if self.member_exists():
      raise ValueError('user is already a member of this team')
    return True
  
  def member_exists(self):
    TeamMember = apps.get_model('meuapp', 'TeamMember')

    try:
        TeamMember.objects.get(team_id=self.team_id, user_id=self.user_id)
        return True
    except TeamMember.DoesNotExist:
        return False
    