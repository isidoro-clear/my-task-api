class TeamValidator:
  def __init__(self, name, description, user_id):
    self.name = name
    self.description = description
    self.user_id = user_id

  def validate(self):
    if not self.name:
      raise ValueError('name is required')
    if not self.user_id:
      raise ValueError('user_id is required')
    return True