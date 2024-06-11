from celery import shared_task
from django.core.mail import send_mail

class SendRemoteNotificationTask:
    @shared_task
    def send_remote_notification(instance, message, payload={}):
      print(f'Sending remote notification: {message}')
      payload_message = "\n".join(f"{key}: {value}" for key, value in payload.items())
      send_mail(
        'Task Notification',
        message + '\n' + payload_message,
        'danilo.santos.clear@gmail.com',
        [instance.email or instance.user.email],
        fail_silently=False,
      )
      pass