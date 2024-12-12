import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        DATABASE=os.environ['DATABASE']
    )

    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import user, home, boosted, gallery
    app.register_blueprint(user.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(boosted.bp)
    app.register_blueprint(gallery.bp)

    return app
