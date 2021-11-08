from django.apps import AppConfig
from django.utils.autoreload import autoreload_started


def watch_extra_files(sender, **kwargs):
    """
    Watch some extra files.

    See https://stackoverflow.com/a/43593959/2720026
    """
    sender.watch_dir('.', '.env')


class SillyPasteConfig(AppConfig):
    name = 'sillypaste'

    def ready(self):
        autoreload_started.connect(watch_extra_files)
