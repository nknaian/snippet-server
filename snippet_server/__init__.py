import random
import time

from flask import Flask
from flask_caching import Cache
from flask_apscheduler import APScheduler

from .config import Config


# Seed random
random.seed(time.time())

# Create cache
cache = Cache()

# Create scheduler
scheduler = APScheduler()


def create_app():
    # Create flask application from config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize cache
    cache.init_app(app)

    # Initialize scheduler and start background tasks
    scheduler.init_app(app)

    from snippet_server.main import background_tasks
    scheduler.start()

    # Register blueprints
    from snippet_server.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app