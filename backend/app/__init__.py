import os
from flask import Flask, render_template
from app.config import config
from app.models import db, migrate
from app.routes import api, cors, jwt, main
from app.schemas import ma


def create_app(test_mode=False):
    """ Create flask application instance """
    app = Flask(__name__)
    if test_mode:
        app.config.from_object(config["test"])
    else:
        env = os.environ.get("FLASK_ENV", "dev")
        app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    app.register_blueprint(main)
    ma.init_app(app)
    api.init_app(app)

    @app.route("/")
    def hello_world():
        return render_template('index.html')

    @app.route('/static/<path:filename>')
    def static_files(filename):
        return app.send_static_file(filename)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('index.html')

    return app
