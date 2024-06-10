from celery import shared_task
from django.core.mail import send_mail

class SendRemoteNotificationTask:
    @shared_task
    def send_remote_notification(instance, message):
      print(f'Sending remote notification: {message}')
      send_mail(
        'Task Notification',
        message,
        'danilo.santos.clear@gmail.com',
        [instance.user.email],
        fail_silently=False,
      )
      pass