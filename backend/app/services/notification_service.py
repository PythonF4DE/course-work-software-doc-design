from app.patterns.strategy.notification_strategy import (
    NotificationStrategy
)


class NotificationService:

    def __init__(
        self,
        strategy: NotificationStrategy
    ):
        self.strategy = strategy

    def set_strategy(
        self,
        strategy: NotificationStrategy
    ):
        self.strategy = strategy

    def notify(
        self,
        recipient,
        message
    ):
        self.strategy.send(
            recipient,
            message
        )