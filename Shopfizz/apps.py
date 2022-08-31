from django.apps import AppConfig


class ShopfizzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Shopfizz'

    def ready(self):
        from Shopfizz import signals