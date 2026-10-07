from abc import ABC, abstractmethod

from app.services.notification_service import (
    NotificationService
)

from app.patterns.strategy.notification_strategy import (
    EmailNotificationStrategy
)


class Observer(ABC):

    @abstractmethod
    def update(self, patient):
        pass


class RegistrationSubject:

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, patient):
        for observer in self._observers:
            observer.update(patient)


class RegistrationNotificationObserver(Observer):

    def update(self, patient):
        notification_service = NotificationService(
            EmailNotificationStrategy()
        )

        notification_service.notify(
            patient.user.email,
            (
                f"Вітаємо, {patient.first_name}! "
                "Ваш обліковий запис успішно створено."
            )
        )