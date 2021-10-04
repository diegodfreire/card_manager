import django
import os
from nameko.extensions import DependencyProvider


class DjangoModels(DependencyProvider):
    def setup(self):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "card_manager.settings"
        )
        django.setup()

    def get_dependency(self, worker_ctx):
        from core import models

        return models

    def worker_teardown(self, worker_ctx):
        django.db.connections.close_all()
