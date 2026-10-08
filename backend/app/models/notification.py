from datetime import datetime, timezone

from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "appointments.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    notification_type = db.Column(
        db.String(30),
        nullable=False
    )

    channel = db.Column(
        db.String(20),
        nullable=False
    )

    sent_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(
            timezone.utc
        )
    )

    appointment = db.relationship(
        "Appointment"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "notification_type":
                self.notification_type,
            "channel": self.channel,
            "sent_at": self.sent_at.isoformat()
        }