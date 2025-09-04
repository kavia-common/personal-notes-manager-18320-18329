from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .config import Config
from .models import db
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.notes import blp as notes_blp


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask application with API blueprints and database."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load config
    app.config.from_object(Config)

    # CORS
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    # OpenAPI configuration
    app.config["API_TITLE"] = app.config.get("API_TITLE", "Notes API")
    app.config["API_VERSION"] = app.config.get("API_VERSION", "v1")
    app.config["OPENAPI_VERSION"] = app.config.get("OPENAPI_VERSION", "3.0.3")
    app.config["OPENAPI_URL_PREFIX"] = app.config.get("OPENAPI_URL_PREFIX", "/docs")
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = app.config.get(
        "OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # Initialize DB
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    # API and blueprints
    api = Api(app)

    # Tag groups
    api.spec.components.schema("Error", {"type": "object"})
    openapi_tags = [
        {"name": "Healt Check", "description": "Health check route"},
        {"name": "Auth", "description": "Authentication endpoints"},
        {"name": "Notes", "description": "Notes management endpoints"},
    ]
    for tag in openapi_tags:
        api.spec.tag(tag)

    # Register blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(notes_blp)

    return app


# For compatibility with run.py importing 'app'
app = create_app()
