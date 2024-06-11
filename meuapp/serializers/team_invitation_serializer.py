class TeamInvitationSerializer:
  def __init__(self, instance):
    self.instance = instance

  def to_json(self):
    return {
      'id': self.instance.id,
      'team_id': self.instance.team_id,
      'email': self.instance.email,
      'status': self.instance.status,
    }
  
  @staticmethod
  def serialize(queryset):
    return [TeamInvitationSerializer(instance).to_json() for instance in queryset]