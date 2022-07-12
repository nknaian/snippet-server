import os
from random import choice
import pathlib

from flask import render_template, url_for

from . import bp


"""HANDLER FUNCTIONS"""


@bp.route('/', methods=['GET', 'POST'])
def index():
    # Pick a random image from the image folder
    image_names = [
        file_name for file_name in os.listdir(os.path.join('snippet_server', 'static', 'images'))
        if pathlib.Path(file_name).suffix == ".jpg"
    ]

    return render_template(
        'main/index.html',
        image_name=choice(image_names) if len(image_names) else None
    )
