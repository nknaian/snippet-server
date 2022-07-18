import os
import random
import time

from flask import Flask

from .config import Config


# Seed random
random.seed(time.time())


def create_app():
    # Create flask application from config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    from snippet_server.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
