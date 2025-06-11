import subprocess
import threading

def start_ffmpeg_stream():
    def run():
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', 'rtsp://username:password!123@103.167.184.133/media/video3',
            '-c:v', 'libx264',
            '-f', 'hls',
            '-hls_time', '2',
            '-hls_list_size', '5',
            '-hls_flags', 'delete_segments',
            'D:/IPCAMERA/media/stream/output.m3u8'
        ]
        subprocess.Popen(ffmpeg_cmd)

    threading.Thread(target=run, daemon=True).start()




