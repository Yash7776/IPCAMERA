from django.db import models

class Project_ip_camera_details_all(models.Model):
    camera_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    ip_link = models.CharField(max_length=300)
    user_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    status = models.IntegerField(default=1)  # 1=active, 0=inactive
    last_connected = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.location_name