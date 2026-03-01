from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
#lalalala
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
   
    db.init_app(app)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app