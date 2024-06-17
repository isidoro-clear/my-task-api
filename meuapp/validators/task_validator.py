class TaskValidator:
  def __init__(self, title, description, user_id, status):
    self.title = title
    self.description = description
    self.user_id = user_id
    self.status = status

  def validate(self):
    if not self.title:
      raise ValueError('title is required')
    if not self.user_id:
      raise ValueError('user_id is required')
    return True