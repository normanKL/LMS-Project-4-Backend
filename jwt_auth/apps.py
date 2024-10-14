from django.apps import AppConfig


class JwtAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jwt_auth'

    def ready(self):
        import jwt_auth.signals 
