from datetime import datetime

from app.extensions import db
from app.models.user import User
from app.models.patient import Patient

from app.patterns.observer.registration_observer import (
    RegistrationSubject,
    RegistrationNotificationObserver
)


class AuthService:

    @staticmethod
    def register_patient(data):
        required_fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "birth_date",
            "password"
        ]

        for field in required_fields:
            if not data.get(field):
                raise ValueError(
                    f"Поле '{field}' є обов'язковим."
                )

        email = data["email"].strip().lower()
        phone = data["phone"].strip()

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            raise ValueError(
                "Користувач з таким e-mail вже існує."
            )

        existing_phone = Patient.query.filter_by(
            phone=phone
        ).first()

        if existing_phone:
            raise ValueError(
                "Пацієнт з таким номером телефону вже існує."
            )

        if len(data["password"]) < 8:
            raise ValueError(
                "Пароль повинен містити щонайменше 8 символів."
            )

        try:
            birth_date = datetime.strptime(
                data["birth_date"],
                "%Y-%m-%d"
            ).date()

        except ValueError:
            raise ValueError(
                "Некоректна дата народження."
            )

        user = User(
            email=email,
            role="patient"
        )

        user.set_password(
            data["password"]
        )

        patient = Patient(
            first_name=data["first_name"].strip(),
            last_name=data["last_name"].strip(),
            middle_name=data.get(
                "middle_name",
                ""
            ).strip() or None,
            phone=phone,
            birth_date=birth_date
        )

        user.patient = patient

        try:
            db.session.add(user)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        registration_subject = RegistrationSubject()

        registration_subject.attach(
            RegistrationNotificationObserver()
        )

        registration_subject.notify(
            patient
        )

        return user, patient