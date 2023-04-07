from flask import Flask

from .api import SECRET_KEY


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from . import views
    app.register_blueprint(views.bp)

    return app