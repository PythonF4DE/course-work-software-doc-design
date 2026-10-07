from abc import ABC


class AppointmentState(ABC):

    name = ""

    def cancel(self, appointment):
        raise ValueError(
            "Цей запис неможливо скасувати."
        )

    def complete(self, appointment):
        raise ValueError(
            "Цей запис неможливо завершити."
        )


class ScheduledState(AppointmentState):

    name = "scheduled"

    def cancel(self, appointment):
        appointment.set_state(
            CancelledState()
        )

    def complete(self, appointment):
        appointment.set_state(
            CompletedState()
        )


class CompletedState(AppointmentState):

    name = "completed"


class CancelledState(AppointmentState):

    name = "cancelled"


def get_appointment_state(status):

    states = {
        "scheduled": ScheduledState(),
        "completed": CompletedState(),
        "cancelled": CancelledState()
    }

    state = states.get(status)

    if not state:
        raise ValueError(
            "Невідомий стан запису."
        )

    return state