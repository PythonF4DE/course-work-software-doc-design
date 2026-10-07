from flask import (
    Blueprint,
    request
)

from app.models.doctor import Doctor
from app.models.specialization import (
    Specialization
)

from app.services.appointment_service import (
    AppointmentService
)


doctors_bp = Blueprint(
    "doctors",
    __name__
)


@doctors_bp.get("")
def get_doctors():

    specialization_id = request.args.get(
        "specialization_id",
        type=int
    )

    query = Doctor.query

    if specialization_id:
        query = query.filter_by(
            specialization_id=
            specialization_id
        )

    doctors = query.order_by(
        Doctor.last_name
    ).all()

    return {
        "doctors": [
            doctor.to_dict()
            for doctor in doctors
        ]
    }


@doctors_bp.get(
    "/specializations"
)
def get_specializations():

    specializations = (
        Specialization.query
        .order_by(
            Specialization.name
        )
        .all()
    )

    return {
        "specializations": [
            item.to_dict()
            for item in specializations
        ]
    }


@doctors_bp.get(
    "/<int:doctor_id>"
)
def get_doctor(doctor_id):

    doctor = Doctor.query.get(
        doctor_id
    )

    if not doctor:
        return {
            "error":
                "Лікаря не знайдено."
        }, 404

    return {
        "doctor":
            doctor.to_dict()
    }


@doctors_bp.get(
    "/<int:doctor_id>/available-slots"
)
def available_slots(doctor_id):

    selected_date = request.args.get(
        "date"
    )

    if not selected_date:
        return {
            "error":
                "Необхідно вказати дату."
        }, 400

    try:
        slots = (
            AppointmentService
            .get_available_slots(
                doctor_id,
                selected_date
            )
        )

        return {
            "doctor_id": doctor_id,
            "date": selected_date,
            "slots": slots
        }

    except ValueError as error:
        return {
            "error": str(error)
        }, 400