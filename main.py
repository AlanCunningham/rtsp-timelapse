import config
import subprocess
import time
from datetime import datetime


def main():
    rtsp_username = config.rtsp_username
    rtsp_password = config.rtsp_password
    rtsp_ip_address = config.rtsp_ip_address
    rtsp_path = f"rtsp://{rtsp_username}:{rtsp_password}@{rtsp_ip_address}/stream1"

    while True:
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                rtsp_path,  # Input path
                "-vframes",
                "1",  # Only grab one frame
                f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.png",  # Output file
            ]
        )
        time.sleep(5)


if __name__ == "__main__":
    main()
