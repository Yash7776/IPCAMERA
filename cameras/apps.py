# apps.py
from django.apps import AppConfig
import sys

class MyAppConfig(AppConfig):
    name = 'cameras'

    def ready(self):
        # Avoid running during migrations, shell, etc.
        if 'runserver' in sys.argv:
            from .streaming import start_ffmpeg_stream
            start_ffmpeg_stream()


