from datetime import (
    datetime,
    timedelta
)

from app.extensions import db

from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.schedule import Schedule
from app.models.appointment import Appointment

from app.patterns.observer.appointment_observer import (
    AppointmentSubject,
    AppointmentNotificationObserver
)


class AppointmentService:

    SLOT_DURATION_MINUTES = 30

    @staticmethod
    def get_available_slots(
        doctor_id,
        date_string
    ):
        try:
            selected_date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            raise ValueError(
                "Некоректний формат дати."
            )

        doctor = db.session.get(
            Doctor,
            doctor_id
        )

        if not doctor:
            raise ValueError(
                "Лікаря не знайдено."
            )

        schedules = Schedule.query.filter_by(
            doctor_id=doctor_id,
            date=selected_date
        ).all()

        if not schedules:
            return []

        appointments = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=selected_date,
            status="scheduled"
        ).all()

        booked_times = {
            appointment.appointment_time.strftime(
                "%H:%M"
            )
            for appointment in appointments
        }

        available_slots = []

        for schedule in schedules:

            current = datetime.combine(
                selected_date,
                schedule.start_time
            )

            end = datetime.combine(
                selected_date,
                schedule.end_time
            )

            while (
                current +
                timedelta(
                    minutes=
                    AppointmentService
                    .SLOT_DURATION_MINUTES
                )
                <= end
            ):
                slot = current.strftime(
                    "%H:%M"
                )

                if slot not in booked_times:
                    available_slots.append(
                        slot
                    )

                current += timedelta(
                    minutes=
                    AppointmentService
                    .SLOT_DURATION_MINUTES
                )

        return sorted(
            set(available_slots)
        )

    @staticmethod
    def create_appointment(
        patient_id,
        data
    ):
        doctor_id = data.get(
            "doctor_id"
        )

        appointment_date = data.get(
            "appointment_date"
        )

        appointment_time = data.get(
            "appointment_time"
        )

        reason = data.get(
            "reason",
            ""
        ).strip()

        if (
            not doctor_id
            or not appointment_date
            or not appointment_time
        ):
            raise ValueError(
                "Лікар, дата та час є обов'язковими."
            )

        doctor = db.session.get(
            Doctor,
            doctor_id
        )

        if not doctor:
            raise ValueError(
                "Лікаря не знайдено."
            )

        patient = db.session.get(
            Patient,
            patient_id
        )

        if not patient:
            raise ValueError(
                "Пацієнта не знайдено."
            )

        try:
            parsed_date = datetime.strptime(
                appointment_date,
                "%Y-%m-%d"
            ).date()

            parsed_time = datetime.strptime(
                appointment_time,
                "%H:%M"
            ).time()

        except ValueError:
            raise ValueError(
                "Некоректна дата або час."
            )

        available_slots = (
            AppointmentService
            .get_available_slots(
                doctor_id,
                appointment_date
            )
        )

        if (
            appointment_time
            not in available_slots
        ):
            raise ValueError(
                "Цей час більше недоступний."
            )

        existing = (
            Appointment.query
            .filter_by(
                doctor_id=doctor_id,
                appointment_date=parsed_date,
                appointment_time=parsed_time,
                status="scheduled"
            )
            .first()
        )

        if existing:
            raise ValueError(
                "Цей час уже зайнятий."
            )

        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=parsed_date,
            appointment_time=parsed_time,
            reason=reason,
            status="scheduled"
        )

        try:
            db.session.add(
                appointment
            )

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        subject = AppointmentSubject()

        subject.attach(
            AppointmentNotificationObserver()
        )

        subject.notify(
            appointment
        )

        return appointment