from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


from config import Config

from werkzeug.debug import DebuggedApplication

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.debug = True

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    return app

app = create_app()
db = SQLAlchemy(app)
db.create_all()

from app import routes, models, forms

