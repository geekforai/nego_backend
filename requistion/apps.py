from django.apps import AppConfig


class RequistionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'requistion'
    def ready(self):
        import requistion.signals