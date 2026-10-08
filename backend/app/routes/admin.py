from datetime import datetime

from flask import (
    Blueprint,
    request
)

from app.extensions import db

from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.specialization import (
    Specialization
)
from app.models.schedule import Schedule

from app.utils.roles import role_required


admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.get("/doctors")
@role_required("admin")
def admin_get_doctors():

    doctors = Doctor.query.order_by(
        Doctor.last_name
    ).all()

    return {
        "doctors": [
            doctor.to_dict()
            for doctor in doctors
        ]
    }


@admin_bp.post("/doctors")
@role_required("admin")
def admin_create_doctor():

    data = request.get_json(
        silent=True
    ) or {}

    required = [
        "first_name",
        "last_name",
        "email",
        "password",
        "specialization_id"
    ]

    for field in required:
        if not data.get(field):
            return {
                "error":
                    f"Поле {field} обов'язкове."
            }, 400


    if User.query.filter_by(
        email=data["email"]
        .strip()
        .lower()
    ).first():

        return {
            "error":
                "Користувач з таким e-mail вже існує."
        }, 400


    specialization = db.session.get(
        Specialization,
        int(
            data[
                "specialization_id"
            ]
        )
    )

    if not specialization:
        return {
            "error":
                "Спеціалізацію не знайдено."
        }, 404


    user = User(
        email=data["email"]
        .strip()
        .lower(),

        role="doctor"
    )

    user.set_password(
        data["password"]
    )


    doctor = Doctor(
        user=user,

        first_name=
            data["first_name"]
            .strip(),

        last_name=
            data["last_name"]
            .strip(),

        description=
            data.get(
                "description",
                ""
            ).strip(),

        specialization_id=
            specialization.id
    )


    db.session.add(
        doctor
    )

    db.session.commit()


    return {
        "message":
            "Лікаря створено.",

        "doctor":
            doctor.to_dict()
    }, 201


@admin_bp.delete(
    "/doctors/<int:doctor_id>"
)
@role_required("admin")
def admin_delete_doctor(
    doctor_id
):

    doctor = db.session.get(
        Doctor,
        doctor_id
    )

    if not doctor:
        return {
            "error":
                "Лікаря не знайдено."
        }, 404


    user = doctor.user


    db.session.delete(
        doctor
    )


    if user:
        db.session.delete(
            user
        )


    db.session.commit()


    return {
        "message":
            "Лікаря видалено."
    }


@admin_bp.get("/patients")
@role_required("admin")
def admin_get_patients():

    patients = Patient.query.order_by(
        Patient.last_name
    ).all()


    return {
        "patients": [
            patient.to_dict()
            for patient in patients
        ]
    }


@admin_bp.get(
    "/specializations"
)
@role_required("admin")
def admin_specializations():

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


@admin_bp.get("/schedule")
@role_required("admin")
def admin_get_schedule():

    schedules = (
        Schedule.query
        .order_by(
            Schedule.date,
            Schedule.start_time
        )
        .all()
    )


    result = []

    for item in schedules:

        result.append({
            **item.to_dict(),

            "doctor": {
                "id":
                    item.doctor.id,

                "full_name":
                    item.doctor
                    .get_full_name()
            }
        })


    return {
        "schedule": result
    }


@admin_bp.post("/schedule")
@role_required("admin")
def admin_create_schedule():

    data = request.get_json(
        silent=True
    ) or {}


    try:

        doctor_id = int(
            data["doctor_id"]
        )

        work_date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()

        start_time = datetime.strptime(
            data["start_time"],
            "%H:%M"
        ).time()

        end_time = datetime.strptime(
            data["end_time"],
            "%H:%M"
        ).time()

    except (
        KeyError,
        ValueError
    ):

        return {
            "error":
                "Некоректні дані розкладу."
        }, 400


    doctor = db.session.get(
        Doctor,
        doctor_id
    )

    if not doctor:

        return {
            "error":
                "Лікаря не знайдено."
        }, 404


    if start_time >= end_time:

        return {
            "error":
                "Час завершення має бути пізніше початку."
        }, 400


    schedule = Schedule(
        doctor_id=doctor_id,
        date=work_date,
        start_time=start_time,
        end_time=end_time
    )


    db.session.add(
        schedule
    )

    db.session.commit()


    return {
        "message":
            "Розклад додано.",

        "schedule":
            schedule.to_dict()
    }, 201


@admin_bp.delete(
    "/schedule/<int:schedule_id>"
)
@role_required("admin")
def admin_delete_schedule(
    schedule_id
):

    schedule = db.session.get(
        Schedule,
        schedule_id
    )

    if not schedule:

        return {
            "error":
                "Запис розкладу не знайдено."
        }, 404


    db.session.delete(
        schedule
    )

    db.session.commit()


    return {
        "message":
            "Розклад видалено."
    }