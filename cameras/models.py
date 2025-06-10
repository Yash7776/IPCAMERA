from django.db import models

# Create your models here.

from django.db import models

class Camera(models.Model):
    project_id = models.CharField(max_length=100)
    camera_id = models.CharField(max_length=100, primary_key=True)
    location_name = models.CharField(max_length=200)
    ip_link = models.URLField()
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.BooleanField(default=True)  # True=operational, False=not working
    last_connected = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.location_name} - {self.camera_id}"
