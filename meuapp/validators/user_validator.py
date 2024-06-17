class UserValidator:
  def __init__(self, first_name, last_name, email, password):
    self.first_name = first_name
    self.last_name = last_name
    self.email = email
    self.password = password

  def validate(self):
    if not self.first_name:
      raise ValueError('first_name is required')
    if not self.last_name:
      raise ValueError('last_name is required')
    if not self.email:
      raise ValueError('email is required')
    if not self.password:
      raise ValueError('password is required')
    return True