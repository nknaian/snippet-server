import os
import glob
import random
import shutil
import pathlib
import datetime
from moviepy.editor import VideoFileClip

from snippet_server import cache, scheduler


'''CONSTANTS'''


CLIP_LENGTH_SEC = 30
SOURCE_MEDIA_DIR = 'media'


'''TASKS'''


@scheduler.task(
    "cron",
    id="refresh_media",
    hour="0",
    minute="0",
    max_instances=1
)
def refresh_media():
    """Update the image and video displayed on the page

    Schedule to occur once a day at 12am
    """
    with scheduler.app.app_context():
        print("Refreshing media...")
        random_image()
        random_video_clip()
        cache.set("refresh_media_datetime", str(datetime.datetime.now()))
        print("Done refreshing media.")


'''HELPER FUNCTIONS'''


def random_image():
    """Refresh the random image in the media directory"""
    # Remove any old movie photos in the media dir
    for file in os.listdir('snippet_server/static/media'):
        if file.endswith(".jpg"):
            os.remove(os.path.join('snippet_server/static/media', file))

    # Get all image file choices
    image_choices = []
    for filename in glob.iglob("{}/**/*.jpg".format(SOURCE_MEDIA_DIR), recursive=True):
        image_choices.append(os.path.abspath(filename))

    if len(image_choices):
        # Choose one of the phots
        image_path = random.choice(image_choices)

        # Copy the image to the media dir
        shutil.copy(image_path, 'snippet_server/static/media')


def random_video_clip():
    """Refresh the random video clip in the media directory"""
    # Remove any old movie files in the media dir
    for file in os.listdir('snippet_server/static/media'):
        if file.endswith(".MP4") or file.endswith(".mp4") or file.endswith(".MOV") or file.endswith(".mov") :
            os.remove(os.path.join('snippet_server/static/media', file))

    # Get all movie file choices
    video_choices = []
    for filename in glob.iglob("{}/**/*.MP4".format(SOURCE_MEDIA_DIR), recursive=True):
        video_choices.append(os.path.abspath(filename))

    for filename in glob.iglob("{}/**/*.mp4".format(SOURCE_MEDIA_DIR), recursive=True):
        video_choices.append(os.path.abspath(filename))

    for filename in glob.iglob("{}/**/*.MOV".format(SOURCE_MEDIA_DIR), recursive=True):
        video_choices.append(os.path.abspath(filename))

    for filename in glob.iglob("{}/**/*.mov".format(SOURCE_MEDIA_DIR), recursive=True):
        video_choices.append(os.path.abspath(filename))

    if len(video_choices):
        # Choose one of the videos
        video_path = random.choice(video_choices)

        # Copy a 30 second (or less) clip from the chosen video to the media folder
        video_clip = VideoFileClip(video_path)
        video_clip_name = ""
        if video_clip.duration <= CLIP_LENGTH_SEC:
            shutil.copy(video_path, 'snippet_server/static/media')
            video_clip_name = os.path.basename(video_path)
        else:
            start = random.randint(0, int(video_clip.duration) - CLIP_LENGTH_SEC)
            end = start + CLIP_LENGTH_SEC
            clip = video_clip.subclip(start, end)
            video_clip_name = "{}_{}_{}.MP4".format(pathlib.Path(video_path).stem, start, end)
            clip.write_videofile(os.path.join('snippet_server/static/media', video_clip_name))
