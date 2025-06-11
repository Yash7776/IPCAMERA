import subprocess
import threading

from cameras.models import Project_ip_camera_details_all

def start_ffmpeg_stream():
    ffmpeg_path = "C:/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe"

    cameras = Project_ip_camera_details_all.objects.filter(status=1)

    for camera in cameras:
        stream_name = f'cam_{camera.camera_id}'
        rtsp_url = f"rtsp://{camera.user_name}:{camera.password}@{camera.ip_link}"
        output_path = f'D:/Yash/IPCAMERA/media/stream/{stream_name}.m3u8'

        def run_ffmpeg(rtsp=rtsp_url, out=output_path):
            cmd = [
                ffmpeg_path,
                '-rtsp_transport', 'tcp',  # use TCP for stability
                '-i', rtsp,
                '-c:v', 'libx264',
                '-f', 'hls',
                '-hls_time', '2',
                '-hls_list_size', '5',
                '-hls_flags', 'delete_segments',
                out
            ]
            subprocess.Popen(cmd)

        threading.Thread(target=run_ffmpeg, daemon=True).start()
