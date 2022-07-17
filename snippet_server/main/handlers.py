import os
import glob
import random
import shutil
import pathlib
from moviepy.editor import VideoFileClip

from flask import render_template, url_for

from . import bp


"""CONSTANTS"""


CLIP_LENGTH_SEC = 30
MEDIA_DIR = 'snippet_server/static/media'
USBDRIVE_DIR = 'usbdrive'  # temp


"""HANDLER FUNCTIONS"""


@bp.route('/', methods=['GET', 'POST'])
def index():
    image_name = random_image()
    video_name = random_video_clip()

    return render_template(
        'main/index.html',
        image_name=image_name,
        video_name=video_name
    )


"""Private Funtions"""


def random_image():
    """Refresh the random image in the media directory
    
    Returns the name of the file created in the media dir
    """
    # Remove any old movie phots in the media dir
    for file in os.listdir(MEDIA_DIR):
        if file.endswith(".jpg"):
            os.remove(os.path.join(MEDIA_DIR, file))

    # Get all image file choices
    image_choices = []
    for filename in glob.iglob('usbdrive/**/*.jpg', recursive=True):
        image_choices.append(os.path.abspath(filename))

    # Choose one of the phots
    image_path = random.choice(image_choices)

    # Copy the image to the media dir
    shutil.copy(image_path, MEDIA_DIR)

    return os.path.basename(image_path)


def random_video_clip():
    """Refresh the random video clip in the media directory
    
    Returns the name of the file created in the media dir
    """
    # Remove any old movie files in the media dir
    for file in os.listdir(MEDIA_DIR):
        if file.endswith(".MP4") or file.endswith(".mov"):
            os.remove(os.path.join(MEDIA_DIR, file))

    # Get all movie file choices
    video_choices = []
    for filename in glob.iglob(f'{USBDRIVE_DIR}/**/*.MP4', recursive=True):
        video_choices.append(os.path.abspath(filename))

    for filename in glob.iglob(f'{USBDRIVE_DIR}/**/*.mov', recursive=True):
        video_choices.append(os.path.abspath(filename))

    # Choose one of the videos
    video_path = random.choice(video_choices)

    # Copy a 30 second (or less) clip from the chosen video to the media folder
    video_clip = VideoFileClip(video_path)
    video_clip_name = ""
    if video_clip.duration <= CLIP_LENGTH_SEC:
        shutil.copy(video_path, MEDIA_DIR)
        video_clip_name = os.path.basename(video_path)
    else:
        start = random.randint(0, int(video_clip.duration) - CLIP_LENGTH_SEC)
        end = start + CLIP_LENGTH_SEC
        clip = video_clip.subclip(start, end)
        video_clip_name = f"{pathlib.Path(video_path).stem}_{start}_{end}.MP4"
        clip.write_videofile(os.path.join(MEDIA_DIR, video_clip_name))

    return video_clip_name
