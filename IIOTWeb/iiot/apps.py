from django.apps import AppConfig


class IiotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iiot'

    # def ready(self):
    #     from .DataCollector import getCollectBySchedule
    #     getCollectBySchedule(1)
        # return super().ready()
