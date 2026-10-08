import os

from datetime import datetime, timedelta

from app.extensions import db

from app.models.appointment import Appointment
from app.models.notification import Notification

from app.services.notification_service import (
    NotificationService
)

from app.patterns.strategy.notification_strategy import (
    EmailNotificationStrategy,
    SmsNotificationStrategy
)


class ReminderService:

    @staticmethod
    def process_reminders():

        reminder_hours = int(
            os.getenv(
                "REMINDER_HOURS_BEFORE",
                "24"
            )
        )

        now = datetime.now()

        reminder_start = (
            now +
            timedelta(
                hours=reminder_hours
            )
        )

        reminder_end = (
            reminder_start +
            timedelta(
                minutes=5
            )
        )


        appointments = (
            Appointment.query
            .filter_by(
                status="scheduled"
            )
            .all()
        )


        for appointment in appointments:

            appointment_datetime = (
                datetime.combine(
                    appointment.appointment_date,
                    appointment.appointment_time
                )
            )


            if not (
                reminder_start
                <= appointment_datetime
                <= reminder_end
            ):
                continue


            already_sent = (
                Notification.query
                .filter_by(
                    appointment_id=
                        appointment.id,

                    notification_type=
                        "appointment_reminder"
                )
                .first()
            )


            if already_sent:
                continue


            ReminderService.send_reminder(
                appointment
            )


    @staticmethod
    def send_reminder(
        appointment
    ):

        patient = appointment.patient
        doctor = appointment.doctor


        message = (
            f"Нагадуємо про прийом до лікаря "
            f"{doctor.get_full_name()} "
            f"{appointment.appointment_date.strftime('%d.%m.%Y')} "
            f"о "
            f"{appointment.appointment_time.strftime('%H:%M')}."
        )


        channel = (
            patient.notification_method
        )


        if channel == "sms":

            strategy = (
                SmsNotificationStrategy()
            )

            recipient = (
                patient.phone
            )

        else:

            strategy = (
                EmailNotificationStrategy()
            )

            recipient = (
                patient.user.email
            )


        notification_service = (
            NotificationService(
                strategy
            )
        )


        notification_service.notify(
            recipient,
            message
        )


        notification = Notification(
            appointment_id=
                appointment.id,

            notification_type=
                "appointment_reminder",

            channel=channel
        )


        db.session.add(
            notification
        )

        db.session.commit()