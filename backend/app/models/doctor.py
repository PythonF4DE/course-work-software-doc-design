from app.extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    specialization_id = db.Column(
        db.Integer,
        db.ForeignKey("specializations.id"),
        nullable=False
    )

    specialization = db.relationship(
        "Specialization",
        back_populates="doctors"
    )

    schedules = db.relationship(
        "Schedule",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    appointments = db.relationship(
        "Appointment",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "description": self.description,
            "specialization": (
                self.specialization.to_dict()
                if self.specialization
                else None
            )
        }