from abc import ABC, abstractmethod


class NotificationStrategy(ABC):

    @abstractmethod
    def send(self, recipient, message):
        pass


class EmailNotificationStrategy(NotificationStrategy):

    def send(self, recipient, message):
        print(
            f"[EMAIL] To: {recipient}\n"
            f"Message: {message}"
        )


class SmsNotificationStrategy(NotificationStrategy):

    def send(self, recipient, message):
        print(
            f"[SMS] To: {recipient}\n"
            f"Message: {message}"
        )