import config
import subprocess
import time
from datetime import datetime


def main():
    rtsp_username = config.rtsp_username
    rtsp_password = config.rtsp_password
    rtsp_ip_address = config.rtsp_ip_address
    rtsp_path = f"rtsp://{rtsp_username}:{rtsp_password}@{rtsp_ip_address}/stream1"

    # Use ffmpeg to connect to the rtsp stream and save 1 frame
    # ffmpeg -i <stream> -vframes 1 <output>
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            rtsp_path,
            "-vframes",
            "1",
            f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.png",
        ]
    )


if __name__ == "__main__":
    main()
