from django.db import models

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  completed = models.BooleanField(default=False)
  user = models.ForeignKey('User', on_delete=models.CASCADE)
  
  def __str__(self):
    return self.title
  
  def to_dict(self):
    return {
      "id": self.id,
      "title": self.title,
      "description": self.description,
      "completed": self.completed,
      "user": self.user.id
    }

  pass