from flask import Blueprint, request

from app.models.doctor import Doctor


doctors_bp = Blueprint(
    "doctors",
    __name__
)


@doctors_bp.get("")
def get_doctors():
    specialization = request.args.get(
        "specialization"
    )

    query = Doctor.query

    if specialization:
        query = query.join(
            Doctor.specialization
        ).filter(
            Doctor.specialization.has(
                name=specialization
            )
        )

    doctors = query.all()

    return {
        "doctors": [
            doctor.to_dict()
            for doctor in doctors
        ]
    }


@doctors_bp.get("/<int:doctor_id>")
def get_doctor(doctor_id):
    doctor = Doctor.query.get(
        doctor_id
    )

    if not doctor:
        return {
            "error": "Лікаря не знайдено."
        }, 404

    return {
        "doctor": doctor.to_dict()
    }