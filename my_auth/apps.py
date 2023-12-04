from django.apps import AppConfig


class MyAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Authentication'
    name = 'my_auth'
