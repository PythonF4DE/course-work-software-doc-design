from datetime import (
    date,
    time,
    timedelta
)

from app import create_app
from app.extensions import db

from app.models.specialization import (
    Specialization
)

from app.models.doctor import Doctor
from app.models.schedule import Schedule


app = create_app()


with app.app_context():

    db.session.query(
        Schedule
    ).delete()

    db.session.query(
        Doctor
    ).delete()

    db.session.query(
        Specialization
    ).delete()

    db.session.commit()

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

    doctors = [
        Doctor(
            first_name="Олександр",
            last_name="Коваль",
            specialization_id=
                cardiology.id,
            description=(
                "Лікар-кардіолог. "
                "Досвід роботи 12 років."
            )
        ),

        Doctor(
            first_name="Ірина",
            last_name="Мельник",
            specialization_id=
                neurology.id,
            description=(
                "Лікар-невролог. "
                "Досвід роботи 9 років."
            )
        ),

        Doctor(
            first_name="Марія",
            last_name="Бондар",
            specialization_id=
                dermatology.id,
            description=(
                "Лікар-дерматолог. "
                "Досвід роботи 7 років."
            )
        ),

        Doctor(
            first_name="Андрій",
            last_name="Шевченко",
            specialization_id=
                therapy.id,
            description=(
                "Сімейний лікар-терапевт. "
                "Досвід роботи 15 років."
            )
        )
    ]

    db.session.add_all(
        doctors
    )

    db.session.flush()

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

            if (
                work_date.weekday()
                < 5
            ):
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