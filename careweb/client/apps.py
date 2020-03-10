from django.apps import AppConfig


class ClientConfig(AppConfig):
    name = 'client'

    def ready(self):
        from client.signals.client_signals import ql_code_signal, adhoc_permission_signal
