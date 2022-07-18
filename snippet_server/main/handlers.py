import os
import glob
import random
import shutil
import pathlib
from moviepy.editor import VideoFileClip

from flask import redirect, render_template, url_for, request

from . import bp
from .decorators import mount_media


"""CONSTANTS"""


CLIP_LENGTH_SEC = 30
SERVE_MEDIA_DIR = 'snippet_server/static/media'
SOURCE_MEDIA_DIR = 'media'


"""HANDLER FUNCTIONS"""


@bp.route('/', methods=['GET', 'POST'])
def index():
    # Get new random image and video clip if it was requested
    # Then redirect to main so that subsequenty page refreshes
    # won't also refresh media
    if request.args.get("refresh_media"):
        random_media()
        return redirect(url_for('main.index'))

    # Get names of all images in static folder
    static_filenames = [file_name for file_name in os.listdir(SERVE_MEDIA_DIR)]
    
    # Get first image in static folder
    image_name = [
        static_filename for static_filename in static_filenames
        if pathlib.Path(static_filename).suffix == ".jpg"
    ][0]

    # Get first video in static folder
    video_name = [
        static_filename for static_filename in static_filenames
        if pathlib.Path(static_filename).suffix in [".MP4", ".mp4", ".MOV", ".mov"]
    ][0]


    return render_template(
        'main/index.html',
        image_name=image_name,
        video_name=video_name
    )


@bp.route('/refresh_media', methods=['GET'])
def refresh_media():
    return render_template('main/refresh_media.html')


"""Private Funtions"""

@mount_media
def random_media():
    """Refresh media, mounting and unmounting storage if necessary"""
    random_image()
    random_video_clip()


def random_image():
    """Refresh the random image in the media directory"""
    # Remove any old movie phots in the media dir
    for file in os.listdir(SERVE_MEDIA_DIR):
        if file.endswith(".jpg"):
            os.remove(os.path.join(SERVE_MEDIA_DIR, file))

    # Get all image file choices
    image_choices = []
    for filename in glob.iglob("{}/**/*.jpg".format(SOURCE_MEDIA_DIR), recursive=True):
        image_choices.append(os.path.abspath(filename))

    # Choose one of the phots
    image_path = random.choice(image_choices)

    # Copy the image to the media dir
    shutil.copy(image_path, SERVE_MEDIA_DIR)


def random_video_clip():
    """Refresh the random video clip in the media directory"""
    # Remove any old movie files in the media dir
    for file in os.listdir(SERVE_MEDIA_DIR):
        if file.endswith(".MP4") or file.endswith(".mp4") or file.endswith(".MOV") or file.endswith(".mov") :
            os.remove(os.path.join(SERVE_MEDIA_DIR, file))

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

    # Choose one of the videos
    video_path = random.choice(video_choices)

    # Copy a 30 second (or less) clip from the chosen video to the media folder
    video_clip = VideoFileClip(video_path)
    video_clip_name = ""
    if video_clip.duration <= CLIP_LENGTH_SEC:
        shutil.copy(video_path, SERVE_MEDIA_DIR)
        video_clip_name = os.path.basename(video_path)
    else:
        start = random.randint(0, int(video_clip.duration) - CLIP_LENGTH_SEC)
        end = start + CLIP_LENGTH_SEC
        clip = video_clip.subclip(start, end)
        video_clip_name = "{}_{}_{}.MP4".format(pathlib.Path(video_path).stem, start, end)
        clip.write_videofile(os.path.join(SERVE_MEDIA_DIR, video_clip_name))
