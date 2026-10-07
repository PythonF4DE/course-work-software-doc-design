from app.extensions import db


class Specialization(db.Model):
    __tablename__ = "specializations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    doctors = db.relationship(
        "Doctor",
        back_populates="specialization"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }