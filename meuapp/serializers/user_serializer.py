class UserSerializer:
  def __init__(self, instance):
    self.instance = instance

  def to_json(self):
    return {
        'id': self.instance.id,
        'first_name': self.instance.first_name,
        'last_name': self.instance.last_name,
        'email': self.instance.email
    }
  
  @staticmethod
  def serialize(queryset):
    return [UserSerializer(instance).to_json() for instance in queryset]