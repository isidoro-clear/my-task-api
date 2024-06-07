from django.db import models
from dotenv import dotenv_values
import datetime
import jwt

class User(models.Model):
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=200)
  token = models.CharField(max_length=200, null=True)

  def __str__(self):
    return self.first_name + ' ' + self.last_name
  
  def token(self):
    env_values = dotenv_values('.env')
    payload = {
      'id': self.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
      'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, env_values['JWT_SECRET_KEY'], algorithm='HS256')