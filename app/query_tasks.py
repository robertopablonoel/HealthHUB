import celery
from celery.task.base import periodic_task, task

# @periodic_task(name="app.query_tasks.queue_reminders", run_every=timedelta(seconds = 20))
@celery.task(name = "demo_task_name")
def queue_reminders():
    print("queuing")
    queue_able = db.session.query(Prescription, User).join(User, (Prescription.user_id == User.user_id)).query.filter((Prescription.last_notification < (datetime.now() - relativedelta(hours = Prescription.frequency))) & (Prescription.notify == True)).all()
    for prescription, user in queue_able:
        current_app.task_queue.enqueue('app.tasks.' + "send_reminders", None, prescription, user)
