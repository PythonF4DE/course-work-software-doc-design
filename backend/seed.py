from datetime import (
    date,
    time,
    timedelta
)

from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.specialization import Specialization
from app.models.doctor import Doctor
from app.models.schedule import Schedule
from app.models.appointment import Appointment


app = create_app()


with app.app_context():

    # Очищаємо старі тестові дані,
    # але не видаляємо зареєстрованих пацієнтів.

    db.session.query(
        Schedule
    ).delete()

    db.session.query(
        Appointment
    ).delete()

    db.session.query(
        Doctor
    ).delete()

    db.session.query(
        User
    ).filter(
        User.role.in_([
            "doctor",
            "admin"
        ])
    ).delete(
        synchronize_session=False
    )

    db.session.query(
        Specialization
    ).delete()

    db.session.commit()


    # -------------------------
    # Спеціалізації
    # -------------------------

    cardiology = Specialization(
        name="Кардіологія"
    )

    neurology = Specialization(
        name="Неврологія"
    )

    dermatology = Specialization(
        name="Дерматологія"
    )

    therapy = Specialization(
        name="Терапія"
    )


    db.session.add_all([
        cardiology,
        neurology,
        dermatology,
        therapy
    ])

    db.session.flush()


    # -------------------------
    # ADMIN
    # -------------------------

    admin_user = User(
        email="admin@medbook.com",
        role="admin"
    )

    admin_user.set_password(
        "Admin123!"
    )

    db.session.add(
        admin_user
    )


    # -------------------------
    # ЛІКАР 1
    # -------------------------

    doctor_user_1 = User(
        email="doctor1@medbook.com",
        role="doctor"
    )

    doctor_user_1.set_password(
        "Doctor123!"
    )

    doctor_1 = Doctor(
        user=doctor_user_1,
        first_name="Олександр",
        last_name="Коваль",
        specialization_id=
            cardiology.id,
        description=(
            "Лікар-кардіолог. "
            "Досвід роботи 12 років."
        )
    )


    # -------------------------
    # ЛІКАР 2
    # -------------------------

    doctor_user_2 = User(
        email="doctor2@medbook.com",
        role="doctor"
    )

    doctor_user_2.set_password(
        "Doctor123!"
    )

    doctor_2 = Doctor(
        user=doctor_user_2,
        first_name="Ірина",
        last_name="Мельник",
        specialization_id=
            neurology.id,
        description=(
            "Лікар-невролог. "
            "Досвід роботи 9 років."
        )
    )


    # -------------------------
    # ЛІКАР 3
    # -------------------------

    doctor_user_3 = User(
        email="doctor3@medbook.com",
        role="doctor"
    )

    doctor_user_3.set_password(
        "Doctor123!"
    )

    doctor_3 = Doctor(
        user=doctor_user_3,
        first_name="Марія",
        last_name="Бондар",
        specialization_id=
            dermatology.id,
        description=(
            "Лікар-дерматолог. "
            "Досвід роботи 7 років."
        )
    )


    # -------------------------
    # ЛІКАР 4
    # -------------------------

    doctor_user_4 = User(
        email="doctor4@medbook.com",
        role="doctor"
    )

    doctor_user_4.set_password(
        "Doctor123!"
    )

    doctor_4 = Doctor(
        user=doctor_user_4,
        first_name="Андрій",
        last_name="Шевченко",
        specialization_id=
            therapy.id,
        description=(
            "Сімейний лікар-терапевт. "
            "Досвід роботи 15 років."
        )
    )


    doctors = [
        doctor_1,
        doctor_2,
        doctor_3,
        doctor_4
    ]


    db.session.add_all(
        doctors
    )

    db.session.flush()


    # -------------------------
    # Розклад лікарів
    # -------------------------

    today = date.today()

    for doctor in doctors:

        for day_number in range(
            1,
            181
        ):

            work_date = (
                today +
                timedelta(
                    days=day_number
                )
            )

            # Понеділок - п'ятниця
            if work_date.weekday() < 5:

                schedule = Schedule(
                    doctor_id=doctor.id,
                    date=work_date,
                    start_time=time(
                        9,
                        0
                    ),
                    end_time=time(
                        17,
                        0
                    )
                )

                db.session.add(
                    schedule
                )


    db.session.commit()


    print(
        "Test data created successfully."
    )

    print()

    print(
        "ADMIN:"
    )

    print(
        "admin@medbook.com"
    )

    print(
        "Admin123!"
    )

    print()

    print(
        "DOCTORS:"
    )

    print(
        "doctor1@medbook.com / Doctor123!"
    )

    print(
        "doctor2@medbook.com / Doctor123!"
    )

    print(
        "doctor3@medbook.com / Doctor123!"
    )

    print(
        "doctor4@medbook.com / Doctor123!"
    )