import apprise
import config
import glob
import os
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
    :returns: The filepath of the timelapse video
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
        timelapse_filepath = f"{timelapse_directory}/forced_fps/{timelapse_filename}"
        subprocess.run(
            [
                "ffmpeg",
                "-r",
                framerate,
                "-pattern_type",
                "glob",
                "-i",
                f"{images_directory}/*.png",
                f"{timelapse_directory}/forced_fps/{timelapse_filename}",
            ]
        )
    else:
        print(f"Creating a normal timelapse")
        timelapse_filename = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.mp4"
        timelapse_filepath = f"{timelapse_directory}/normal_fps/{timelapse_filename}"
        subprocess.run(
            [
                "ffmpeg",
                "-pattern_type",
                "glob",
                "-i",
                f"{images_directory}/*.png",
                f"{timelapse_directory}/normal_fps/{timelapse_filename}",
            ]
        )
    return timelapse_filepath


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
    image_files = glob.glob1(images_directory, "*.png")
    expected_number_of_photos = len(image_files)
    if len(image_files) == expected_number_of_photos:
        # Create the timelapse
        normal_timelapse_filepath = create_timelapse()
        forced_fps_timelapse_filepath = create_timelapse(force_framerate=True)

        # Create an Apprise instance
        app = apprise.Apprise()

        for service in config.apprise_services:
            app.add(service)

        attachments = [
            normal_timelapse_filepath,
            forced_fps_timelapse_filepath,
        ]

        # Send the message to the Apprise services
        print(f"Sending notification with {attachments}")
        app.notify(body="Weekly timelapse", title="Timelapse", attach=attachments)

        # Delete the images
        print("Starting deletion")
        for image_file in image_files:
            image_filepath = f"{images_directory}/{image_file}"
            if os.path.exists(image_filepath):
                print(f"Deleting {image_filepath}")
                os.remove(image_filepath)


if __name__ == "__main__":
    main()
