from datetime import date

from flask import Blueprint

from flask_jwt_extended import (
    get_jwt_identity
)

from app.extensions import db

from app.models.user import User
from app.models.appointment import Appointment
from app.models.schedule import Schedule

from app.utils.roles import role_required


doctor_dashboard_bp = Blueprint(
    "doctor_dashboard",
    __name__
)


@doctor_dashboard_bp.get("/profile")
@role_required("doctor")
def doctor_profile():

    user_id = int(
        get_jwt_identity()
    )

    user = db.session.get(
        User,
        user_id
    )

    if (
        not user
        or not user.doctor
    ):
        return {
            "error":
                "Профіль лікаря не знайдено."
        }, 404

    return {
        "doctor":
            user.doctor.to_dict()
    }


@doctor_dashboard_bp.get(
    "/appointments"
)
@role_required("doctor")
def doctor_appointments():

    user_id = int(
        get_jwt_identity()
    )

    user = db.session.get(
        User,
        user_id
    )

    if (
        not user
        or not user.doctor
    ):
        return {
            "error":
                "Профіль лікаря не знайдено."
        }, 404

    appointments = (
        Appointment.query
        .filter_by(
            doctor_id=user.doctor.id
        )
        .order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        )
        .all()
    )

    result = []

    for appointment in appointments:

        patient = appointment.patient

        result.append({
            **appointment.to_dict(),

            "patient": {
                "id": patient.id,
                "full_name":
                    patient.get_full_name(),
                "phone":
                    patient.phone,
                "email":
                    patient.user.email
            }
        })

    return {
        "appointments": result
    }


@doctor_dashboard_bp.get(
    "/schedule"
)
@role_required("doctor")
def doctor_schedule():

    user_id = int(
        get_jwt_identity()
    )

    user = db.session.get(
        User,
        user_id
    )

    if (
        not user
        or not user.doctor
    ):
        return {
            "error":
                "Профіль лікаря не знайдено."
        }, 404

    schedules = (
        Schedule.query
        .filter_by(
            doctor_id=user.doctor.id
        )
        .filter(
            Schedule.date >= date.today()
        )
        .order_by(
            Schedule.date
        )
        .all()
    )

    return {
        "schedule": [
            item.to_dict()
            for item in schedules
        ]
    }


@doctor_dashboard_bp.patch(
    "/appointments/<int:appointment_id>/complete"
)
@role_required("doctor")
def complete_appointment(
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
                "Прийом не знайдено."
        }, 404

    if (
        not user.doctor
        or appointment.doctor_id
        != user.doctor.id
    ):
        return {
            "error":
                "Немає доступу до цього прийому."
        }, 403

    try:
        appointment.complete()

        db.session.commit()

        return {
            "message":
                "Прийом завершено.",

            "appointment":
                appointment.to_dict()
        }

    except ValueError as error:
        return {
            "error":
                str(error)
        }, 400