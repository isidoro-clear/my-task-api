from meuapp.serializers.team_member_serializer import TeamMemberSerializer

class TeamSerializer:
    def __init__(self, instance):
        self.instance = instance

    def to_json(self):
        return {
            'id': self.instance.id,
            'name': self.instance.name,
            'description': self.instance.description,
            'user_id': self.instance.user_id,
            'team_members': TeamMemberSerializer.serialize(self.instance.teammember_set.all())
        }
    
    @staticmethod
    def serialize(queryset):
        return [TeamSerializer(instance).to_json() for instance in queryset]