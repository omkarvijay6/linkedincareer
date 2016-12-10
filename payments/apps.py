from __future__ import unicode_literals

from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'payments'

    def ready(self):
        from payments import signals
