from django.shortcuts import render, redirect, get_object_or_404
from .models import Project_ip_camera_details_all
from django.contrib import messages
from django.utils import timezone

def stream_camera(request):
    cameras = Project_ip_camera_details_all.objects.filter(status=1)
    return render(request, 'camera_view.html', {'cameras': cameras})

def add_camera(request):
    if request.method == "POST":
        location_name = request.POST.get('location_name')
        ip_link = request.POST.get('ip_link')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        if not all([location_name, ip_link, user_name, password]):
            messages.error(request, "All fields are required.")
            return redirect('stream_camera')

        # Create new camera entry
        Project_ip_camera_details_all.objects.create(
            location_name=location_name,
            ip_link=ip_link,
            user_name=user_name,
            password=password,
            status=1,
            last_connected=timezone.now()
        )
        messages.success(request, "Camera added successfully.")
        return redirect('stream_camera')
    else:
        return redirect('stream_camera')

def delete_camera(request, camera_id):
    camera = get_object_or_404(Project_ip_camera_details_all, pk=camera_id)
    camera.delete()
    messages.success(request, f"Camera {camera.location_name} deleted successfully.")
    return redirect('stream_camera')
