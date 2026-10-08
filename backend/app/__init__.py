from flask import Flask
from flask_cors import CORS

from config import Config
from app.extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(
        app,
        origins=[app.config["FRONTEND_URL"]],
        supports_credentials=True
    )

    from app.routes.auth import auth_bp
    from app.routes.doctors import doctors_bp

    from app.routes.appointments import (
        appointments_bp
    )

    from app.scheduler import start_scheduler

    app.register_blueprint(
        appointments_bp,
        url_prefix="/api/appointments"
    )

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        doctors_bp,
        url_prefix="/api/doctors"
    )

    @app.get("/api/health")
    def health():
        return {
            "status": "ok",
            "message": "Doctor Appointment API is running"
        }

    start_scheduler(app)

    return app