from abc import ABC, abstractmethod

from app.services.notification_service import (
    NotificationService
)

from app.patterns.strategy.notification_strategy import (
    EmailNotificationStrategy
)


class AppointmentObserver(ABC):

    @abstractmethod
    def update(self, appointment):
        pass


class AppointmentSubject:

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(
            observer
        )

    def notify(self, appointment):
        for observer in self._observers:
            observer.update(
                appointment
            )


class AppointmentNotificationObserver(
    AppointmentObserver
):

    def update(self, appointment):

        notification_service = (
            NotificationService(
                EmailNotificationStrategy()
            )
        )

        patient = appointment.patient
        doctor = appointment.doctor

        message = (
            f"Ваш запис до лікаря "
            f"{doctor.get_full_name()} "
            f"створено на "
            f"{appointment.appointment_date} "
            f"о "
            f"{appointment.appointment_time.strftime('%H:%M')}."
        )

        notification_service.notify(
            patient.user.email,
            message
        )