import os
from flask import Flask, request, jsonify
from app.routes import register_routes
from app.extensions import db
from app.config import Config

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    db.init_app(app)
    with app.app_context():
        db.create_all()

    register_routes(app)

    return app