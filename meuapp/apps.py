from django.apps import AppConfig
from django.core.signals import setting_changed


class MeuappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meuapp'

    def ready(self):
        from meuapp.signals import task_signals
        setting_changed.connect(task_signals.task_post_save)
        pass
