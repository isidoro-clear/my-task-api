class TeamMemberSerializer:
    def __init__(self, instance):
        self.instance = instance

    def to_json(self):
        return {
            'id': self.instance.id,
            'team_id': self.instance.team_id,
            'user_id': self.instance.user_id,
            'role': self.instance.role,
        }
    
    @staticmethod
    def serialize(queryset):
        return [TeamMemberSerializer(instance).to_json() for instance in queryset]