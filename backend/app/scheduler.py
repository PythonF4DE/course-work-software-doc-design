from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from app.services.reminder_service import (
    ReminderService
)


scheduler = BackgroundScheduler()


def start_scheduler(app):

    if scheduler.running:
        return


    def reminder_job():

        with app.app_context():

            try:
                ReminderService.process_reminders()

            except Exception as error:

                print(
                    "Reminder scheduler error:",
                    error
                )


    scheduler.add_job(
        reminder_job,
        trigger="interval",
        minutes=5,
        id="appointment_reminders",
        replace_existing=True
    )


    scheduler.start()