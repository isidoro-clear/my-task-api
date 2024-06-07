class TaskSerializer:
    def __init__(self, instance):
        self.instance = instance

    def to_json(self):
        return {
            'id': self.instance.id,
            'title': self.instance.title,
            'description': self.instance.description,
            'completed': self.instance.completed
        }
    
    @staticmethod
    def serialize(queryset):
        return [TaskSerializer(instance).to_json() for instance in queryset]