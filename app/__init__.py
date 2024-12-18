from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)

    db.init_app(app)

    # Import and register blueprints
    from app.routes.user_routes import user_routes
    app.register_blueprint(user_routes)

    return app
