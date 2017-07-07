from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        # Create default api key, it hardcoded in frontend config.js
        from rest_framework_api_key.models import APIKey
        try:
            APIKey.objects.get_or_create(
                name='default',
                key='051c00dbdb8686e95e56c8d18e3fb37f274f41c5'
            )
        except:
            pass