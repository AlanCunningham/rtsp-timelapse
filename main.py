import apprise
import config
import glob
import subprocess
from datetime import datetime


images_directory = "input"
timelapse_directory = "output"


def create_timelapse(force_framerate=False):
    """
    Uses ffmpeg to stitch all images in a directory (in datetime order) together
    to make a timelapse.
    :param force_framerate: Force the output to run at a different framerate
    than default (which is 24fps). If this is True, the output will be forced to
    60fps.
    :returns: The filename of the timelapse video
    """
    # Use ffmpeg to stitch the images together into a timelapse
    # ffmpeg -pattern_type glob -i "*.png" output/<output>
    # ffmpeg -r 60 -pattern_type glob -i "*.png" output/<output>
    if force_framerate:
        framerate = "60"
        print(f"Creating timelapse at {framerate}fps")
        timelapse_filename = (
            f"{datetime.now().strftime('%Y%m%d-%H%M%S')}_fps_{framerate}.mp4"
        )
        subprocess.run(
            [
                "ffmpeg",
                "-r",
                framerate,
                "-pattern_type",
                "glob",
                "-i",
                f"{images_directory}/*.png",
                f"{timelapse_directory}/{datetime.now().strftime('%Y%m%d-%H%M%S')}_fps_{framerate}.mp4",
            ]
        )
    else:
        print(f"Creating a normal timelapse")
        timelapse_filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp4"
        subprocess.run(
            [
                "ffmpeg",
                "-pattern_type",
                "glob",
                "-i",
                f"{images_directory}/*.png",
                f"{timelapse_directory}/{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp4",
            ]
        )
    return timelapse_filename


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
            f"{images_directory}/{datetime.now().strftime('%Y%m%d-%H%M%S')}.png",
        ]
    )

    # Only create a timelapse once we have a weeks worth of photos
    image_counter = len(glob.glob1(images_directory, "*.png"))
    expected_number_of_photos = 168
    if image_counter == expected_number_of_photos:
        # Create the timelapse
        normal_timelapse_filename = create_timelapse()
        forced_fps_timelapse_filename = create_timelapse(force_framerate=True)

        # Create an Apprise instance
        app = apprise.Apprise()

        for service in config.apprise_services:
            app.add(service)

        attachments = [
            f"{timelapse_directory}/{normal_timelapse_filename}",
            f"{timelapse_directory}/{forced_fps_timelapse_filename}",
        ]

        # Send the message to the Apprise services
        app.notify(body="Timelapse", title="app_title", attach=attachments)


if __name__ == "__main__":
    main()
