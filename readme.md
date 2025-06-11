Run This Command To See Live Feed

ffmpeg -i "rtsp://username:password!123@103.167.184.133/media/video3" ^
-c:v libx264 -f hls -hls_time 2 -hls_list_size 5 -hls_flags delete_segments ^
"D:\IPCAMERA\media\stream\output.m3u8"
