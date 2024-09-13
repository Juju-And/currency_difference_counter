from flask import Flask
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__, template_folder='templates')
    app.config["SECRET_KEY"] = "44cc17091493574f"



    # Please adjust accordingly
    POSTGRES = {
        "user": "postgres",
        "pw": "coderslab",
        "db": "currencyrates",
        "host": "localhost",
        "port": "5432",
    }
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app