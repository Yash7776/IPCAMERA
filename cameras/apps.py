from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'cameras'

    def ready(self):
        from .streaming import start_ffmpeg_stream
        start_ffmpeg_stream()

