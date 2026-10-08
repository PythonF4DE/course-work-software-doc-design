from app.extensions import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    middle_name = db.Column(
        db.String(100),
        nullable=True
    )

    phone = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    birth_date = db.Column(
        db.Date,
        nullable=False
    )

    notification_method = db.Column(
        db.String(20),
        nullable=False,
        default="email"
    )

    user = db.relationship(
        "User",
        back_populates="patient"
    )

    appointments = db.relationship(
        "Appointment",
        back_populates="patient",
        cascade="all, delete-orphan"
    )

    def get_full_name(self):
        parts = [
            self.last_name,
            self.first_name,
            self.middle_name
        ]

        return " ".join(
            part for part in parts if part
        )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "full_name": self.get_full_name(),
            "phone": self.phone,
            "birth_date": self.birth_date.isoformat(),
            "email": self.user.email,
            "notification_method": self.notification_method,
        }