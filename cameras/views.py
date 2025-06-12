import requests
import subprocess
import threading
import os
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from urllib.parse import unquote
from .models import Project_ip_camera_details_all

def stream_camera(request):
    cameras = Project_ip_camera_details_all.objects.all()
    return render(request, 'cameras/camera_view.html', {'cameras': cameras})

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

        # # Attempt to connect to the camera (basic validation)
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

        # Start FFmpeg stream for the new camera
        ffmpeg_path = "C:/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe"
        media_dir = "D:/Yash/IPCAMERA/media/stream"
        os.makedirs(media_dir, exist_ok=True)
        stream_name = f'cam_{camera.camera_id}'
        rtsp_url = f"rtsp://{camera.user_name}:{camera.password}@{camera.ip_link}"
        output_path = os.path.join(media_dir, f"{stream_name}.m3u8")

        def run_ffmpeg(rtsp=rtsp_url, out=output_path, cam=camera):
            try:
                cmd = [
                    ffmpeg_path,
                    '-rtsp_transport', 'tcp',
                    '-i', rtsp,
                    '-c:v', 'libx264',
                    '-f', 'hls',
                    '-hls_time', '2',
                    '-hls_list_size', '5',
                    '-hls_flags', 'delete_segments',
                    out
                ]
                process = subprocess.Popen(cmd)
                # Non-blocking, no communicate() to avoid delays
                cam.status = 1
                cam.last_connected = timezone.now()
                cam.save()
            except Exception as e:
                print(f"Error streaming camera {cam.camera_id}: {str(e)}")
                cam.status = 0
                cam.last_connected = None
                cam.save()

        threading.Thread(target=run_ffmpeg, daemon=True).start()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

def delete_camera(request, camera_id):
    try:
        camera = Project_ip_camera_details_all.objects.get(camera_id=unquote(camera_id))
        camera.delete()
    except Project_ip_camera_details_all.DoesNotExist:
        pass
    return redirect('stream_camera')