from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .sendmail import send_mail_page
import pytz

scheduler_started = False

def start():
    print("hehrehfvh")
    global scheduler_started

    if scheduler_started:
        return
    timezone = pytz.timezone("Asia/Kolkata")

    scheduler = BackgroundScheduler(timezone=timezone)

    scheduler.add_job(
        send_mail_page,
        trigger=CronTrigger(day="20", hour="17", minute="30"),
        id="send_mail_page",
        replace_existing=True,
    )

    # Start the scheduler
    scheduler.start()
    scheduler_started = True

start()
