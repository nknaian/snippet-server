import os
import pathlib

from flask import render_template

from . import bp


"""HANDLER FUNCTIONS"""


@bp.route('/', methods=['GET', 'POST'])
def index():
    # Get names of all images in static folder
    static_filenames = [file_name for file_name in os.listdir('snippet_server/static/media')]
    
    # Get first image in static folder
    try:
        image_name = [
            static_filename for static_filename in static_filenames
            if pathlib.Path(static_filename).suffix == ".jpg"
        ][0]
    except IndexError:
        image_name = None

    # Get first video in static folder
    try:
        video_name = [
            static_filename for static_filename in static_filenames
            if pathlib.Path(static_filename).suffix in [".MP4", ".mp4", ".MOV", ".mov"]
        ][0]
    except IndexError:
        video_name = None


    return render_template(
        'main/index.html',
        image_name=image_name,
        video_name=video_name
    )


@bp.route('/refresh_media', methods=['GET'])
def refresh_media():
    return render_template('main/refresh_media.html')
