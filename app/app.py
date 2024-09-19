from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()

def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config["SECRET_KEY"] = "44cc17091493574f"
    # app.secret_key = "SOME KEY"


    # Please adjust accordingly
    POSTGRES = {
        "user": os.environ.get("user"),
        "pw": os.environ.get("pw"),
        "db": os.environ.get("db"),
        "host": os.environ.get("host"),
        "port": os.environ.get("port")
    }
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)

    @login_manager.unauthorized_handler
    def unauthorised_callback():
        return redirect(url_for('index'))

    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app
