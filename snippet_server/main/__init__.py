from flask import Blueprint


bp = Blueprint('main', __name__)


from snippet_server.main import handlers
