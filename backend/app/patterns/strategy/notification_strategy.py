from abc import ABC, abstractmethod

import os
import smtplib

from email.mime.text import MIMEText

from twilio.rest import Client


class NotificationStrategy(ABC):

    @abstractmethod
    def send(
        self,
        recipient,
        message
    ):
        pass


class EmailNotificationStrategy(
    NotificationStrategy
):

    def send(
        self,
        recipient,
        message
    ):
        smtp_host = os.getenv(
            "SMTP_HOST"
        )

        smtp_port = int(
            os.getenv(
                "SMTP_PORT",
                "587"
            )
        )

        smtp_user = os.getenv(
            "SMTP_USER"
        )

        smtp_password = os.getenv(
            "SMTP_PASSWORD"
        )

        smtp_from = os.getenv(
            "SMTP_FROM"
        ) or smtp_user


        if (
            not smtp_user
            or not smtp_password
        ):
            print(
                "\n[EMAIL REMINDER]"
            )

            print(
                f"To: {recipient}"
            )

            print(
                f"Message: {message}"
            )

            return


        email = MIMEText(
            message,
            "plain",
            "utf-8"
        )

        email["Subject"] = (
            "Нагадування про прийом"
        )

        email["From"] = smtp_from
        email["To"] = recipient


        with smtplib.SMTP(
            smtp_host,
            smtp_port
        ) as server:

            server.starttls()

            server.login(
                smtp_user,
                smtp_password
            )

            server.send_message(
                email
            )


class SmsNotificationStrategy(
    NotificationStrategy
):

    def send(
        self,
        recipient,
        message
    ):
        account_sid = os.getenv(
            "TWILIO_ACCOUNT_SID"
        )

        auth_token = os.getenv(
            "TWILIO_AUTH_TOKEN"
        )

        phone_number = os.getenv(
            "TWILIO_PHONE_NUMBER"
        )


        if (
            not account_sid
            or not auth_token
            or not phone_number
        ):
            print(
                "\n[SMS REMINDER]"
            )

            print(
                f"To: {recipient}"
            )

            print(
                f"Message: {message}"
            )

            return


        client = Client(
            account_sid,
            auth_token
        )

        client.messages.create(
            body=message,
            from_=phone_number,
            to=recipient
        )