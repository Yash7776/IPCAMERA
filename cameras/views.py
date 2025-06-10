import requests
from django.http import StreamingHttpResponse
from requests.auth import HTTPBasicAuth
from django.shortcuts import render


def stream_camera(request):
    return render(request, 'camera_view.html')