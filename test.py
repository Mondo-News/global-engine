from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from controller.controller import controllerObject

sched = BlockingScheduler()


def update_data():
    print("Daily data Update at 9 o'clock started...")
    print("Daily data update finished successfully!")


sched.add_job(update_data, CronTrigger.from_crontab('* * * * *'))
sched.start()
