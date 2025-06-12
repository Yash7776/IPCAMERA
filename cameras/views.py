import requests
from django.http import StreamingHttpResponse, JsonResponse
from requests.auth import HTTPBasicAuth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Project_ip_camera_details_all

def stream_camera(request):
    cameras = Project_ip_camera_details_all.objects.filter(status=1)
    # Group cameras by location_name
    cameras_by_location = {}
    for cam in cameras:
        location = cam.location_name or "Default Location"
        if location not in cameras_by_location:
            cameras_by_location[location] = []
        cameras_by_location[location].append(cam)
    return render(request, 'camera_view.html', {'cameras_by_location': cameras_by_location})

@csrf_exempt
def add_camera(request):
    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        ip_link = request.POST.get('ip_link')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        # Validate input
        if not all([location_name, ip_link, user_name, password]):
            return JsonResponse({'success': False, 'error': 'All fields are required.'})

        # Attempt to connect to the camera (basic validation)
        # try:
        #     response = requests.get(ip_link, auth=HTTPBasicAuth(user_name, password), timeout=5)
        #     if response.status_code != 200:
        #         return JsonResponse({'success': False, 'error': 'Could not connect to camera.'})
        # except requests.exceptions.RequestException:
        #     return JsonResponse({'success': False, 'error': 'Invalid stream URL or credentials.'})

        # Save new camera
        camera = Project_ip_camera_details_all(
            location_name=location_name,
            ip_link=ip_link,
            user_name=user_name,
            password=password,
            status=1
        )
        camera.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

def delete_camera(request, camera_id):
    try:
        camera = Project_ip_camera_details_all.objects.get(camera_id=camera_id)
        camera.delete()
    except Project_ip_camera_details_all.DoesNotExist:
        pass
    return redirect('stream_camera')