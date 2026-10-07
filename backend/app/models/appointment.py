from datetime import datetime, timezone

from app.extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "patients.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "doctors.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    appointment_date = db.Column(
        db.Date,
        nullable=False
    )

    appointment_time = db.Column(
        db.Time,
        nullable=False
    )

    reason = db.Column(
        db.String(500),
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="scheduled"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    patient = db.relationship(
        "Patient",
        back_populates="appointments"
    )

    doctor = db.relationship(
        "Doctor",
        back_populates="appointments"
    )

    def set_state(self, state):
        self.status = state.name

    def cancel(self):
        from app.patterns.state.appointment_state import (
            get_appointment_state
        )

        state = get_appointment_state(
            self.status
        )

        state.cancel(self)

    def complete(self):
        from app.patterns.state.appointment_state import (
            get_appointment_state
        )

        state = get_appointment_state(
            self.status
        )

        state.complete(self)

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "doctor": (
                self.doctor.to_dict()
                if self.doctor
                else None
            ),
            "appointment_date":
                self.appointment_date.isoformat(),
            "appointment_time":
                self.appointment_time.strftime("%H:%M"),
            "reason": self.reason,
            "status": self.status,
            "created_at":
                self.created_at.isoformat()
        }