from flask import (
    Blueprint,
    request
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db
from app.models.user import User
from app.models.appointment import Appointment

from app.services.appointment_service import (
    AppointmentService
)


appointments_bp = Blueprint(
    "appointments",
    __name__
)


@appointments_bp.post("")
@jwt_required()
def create_appointment():

    user_id = int(
        get_jwt_identity()
    )

    user = db.session.get(
        User,
        user_id
    )

    if (
        not user
        or not user.patient
    ):
        return {
            "error":
                "Профіль пацієнта не знайдено."
        }, 404

    data = request.get_json(
        silent=True
    ) or {}

    try:
        appointment = (
            AppointmentService
            .create_appointment(
                user.patient.id,
                data
            )
        )

        return {
            "message":
                "Запис успішно створено.",
            "appointment":
                appointment.to_dict()
        }, 201

    except ValueError as error:
        return {
            "error":
                str(error)
        }, 400


@appointments_bp.get("")
@jwt_required()
def get_my_appointments():

    user_id = int(
        get_jwt_identity()
    )

    user = db.session.get(
        User,
        user_id
    )

    if (
        not user
        or not user.patient
    ):
        return {
            "error":
                "Пацієнта не знайдено."
        }, 404

    appointments = (
        Appointment.query
        .filter_by(
            patient_id=
            user.patient.id
        )
        .order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        )
        .all()
    )

    return {
        "appointments": [
            item.to_dict()
            for item in appointments
        ]
    }


@appointments_bp.patch(
    "/<int:appointment_id>/cancel"
)
@jwt_required()
def cancel_appointment(
    appointment_id
):

    user_id = int(
        get_jwt_identity()
    )

    user = db.session.get(
        User,
        user_id
    )

    appointment = db.session.get(
        Appointment,
        appointment_id
    )

    if not appointment:
        return {
            "error":
                "Запис не знайдено."
        }, 404

    if (
        not user.patient
        or appointment.patient_id
        != user.patient.id
    ):
        return {
            "error":
                "Немає доступу до цього запису."
        }, 403

    try:
        appointment.cancel()

        db.session.commit()

        return {
            "message":
                "Запис скасовано.",
            "appointment":
                appointment.to_dict()
        }

    except ValueError as error:
        return {
            "error":
                str(error)
        }, 400