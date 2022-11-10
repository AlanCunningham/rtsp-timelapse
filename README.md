# RTSP Timelapse

Connects to an RTSP stream, takes a photo, and stitches it together to make a timelapse.
Then sends a the timelapse video to your favourite service [using Apprise](https://github.com/caronc/apprise).

## Hardware
- Personally, I have this running on a Raspberry Pi (any model will probably do)
- An IP camera that supports RTSP

## Installation
- Create a python3 virtual environment and install the project's requirements:
```
$ python3 -m venv rtsp_timelapse
$ source rtsp_timelapse/bin/activate
(rtsp_timelapse) $ pip install -r requirements.txt
```
- You will also need [ffmpeg](https://ffmpeg.org/) installed on your machine.  This can usually be
installed using a package manager.  For example:
```
$ sudo apt-get install ffmpeg
```
- Open config.py and enter the camera's
  - RTSP username
  - RTSP password
  - IP address
- Also in config.py, enter where you want your timelapse videos to be sent. See
[Apprise's github page](https://github.com/caronc/apprise) for examples. An
example for Telegram and Discord would look something like this:
```
# The list of services to notify
apprise_services = [
    "tgram://bottoken/ChatID",
    "discord://webhook_id/webhook_token",
]
```
- You should now be able to start the program:
```
(rtsp_timelapse) $ python main.py
```

# Creating the timelapses
The script is intended to be run regularly on a cronjob.  It will connect to the IP camera, take a photo 
and save the image to the **input** folder.

Once a week's worth of photos have been taken, the script will stitch the photos together using
[ffmpeg](https://ffmpeg.org/) and save the video to the **output** directory.  Once saved, it will send the videos to
the Apprise services set in config.py.  The images used to create the timelapse will then be
deleted.

Two copies of the timelapse will be created in the **output** directory.
- normal_timelapse - This contains timelapses at the default framerate - 24fps
- forced_fps - This contains timelapses at a framerate of 60fps
