from flask import Flask
import os

import view

def create_app(deployment=False):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile(os.path.join(app.root_path, "config.py"))
    if deployment:
        app.config.from_pyfile("config.py", silent=True)


    from database import init_db
    init_db(app)

    from blueprint import api
    app.register_blueprint(api)

    return app