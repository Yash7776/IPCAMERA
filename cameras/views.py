import requests
from django.http import StreamingHttpResponse
from requests.auth import HTTPBasicAuth
from django.shortcuts import render

from .models import Project_ip_camera_details_all

def stream_camera(request):
    cameras = Project_ip_camera_details_all.objects.filter(status=1)
    return render(request, 'camera_view.html', {'cameras': cameras})
