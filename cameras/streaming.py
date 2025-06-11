import subprocess
import threading

def start_ffmpeg_stream():
    ffmpeg_path = "C:/ffmpeg-7.1.1-full_build/bin/ffmpeg.exe"  # ✅ Change if needed

    # 🟢 Add all your camera streams here
    cameras = {
        'cam1': 'rtsp://username:password!123@103.167.184.133:554/media/video1',
        'cam2': 'rtsp://username:password!123@103.167.184.133:554/media/video2',
        'cam3': 'rtsp://username:password!123@103.167.184.133:554/media/video3',
    }

    # 🔁 Loop through each camera and start FFmpeg
    for name, url in cameras.items():
        output_path = f'D:/Yash/IPCAMERA/media/stream/{name}.m3u8'

        def run_ffmpeg(rtsp_url=url, out=output_path):
            cmd = [
                ffmpeg_path,
                '-i', rtsp_url,
                '-c:v', 'libx264',
                '-f', 'hls',
                '-hls_time', '2',
                '-hls_list_size', '5',
                '-hls_flags', 'delete_segments',
                out
            ]
            subprocess.Popen(cmd)

        threading.Thread(target=run_ffmpeg, daemon=True).start()