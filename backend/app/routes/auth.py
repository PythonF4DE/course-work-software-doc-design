from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from app.models.user import User
from app.services.auth_service import AuthService


auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.post("/register")
def register():
    data = request.get_json(
        silent=True
    ) or {}

    try:
        user, patient = (
            AuthService.register_patient(data)
        )

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return {
            "message": (
                "Пацієнта успішно зареєстровано."
            ),
            "access_token": access_token,
            "user": user.to_dict(),
            "patient": patient.to_dict()
        }, 201

    except ValueError as error:
        return {
            "error": str(error)
        }, 400

    except Exception as error:
        print(error)

        return {
            "error": (
                "Внутрішня помилка сервера."
            )
        }, 500


@auth_bp.post("/login")
def login():
    data = request.get_json(
        silent=True
    ) or {}

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    if not email or not password:
        return {
            "error": (
                "Введіть e-mail та пароль."
            )
        }, 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user or not user.check_password(
        password
    ):
        return {
            "error": (
                "Неправильний e-mail або пароль."
            )
        }, 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return {
        "message": "Вхід виконано успішно.",
        "access_token": access_token,
        "user": user.to_dict(),
        "patient": (
            user.patient.to_dict()
            if user.patient
            else None
        )
    }


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.get(
        int(user_id)
    )

    if not user:
        return {
            "error": "Користувача не знайдено."
        }, 404

    return {
        "user": user.to_dict(),
        "patient": (
            user.patient.to_dict()
            if user.patient
            else None
        )
    }