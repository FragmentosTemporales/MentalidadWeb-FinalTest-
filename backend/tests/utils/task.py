from app.models import Task


def save_task_to_db(data):
    """ Save task to db """
    task = Task(**data)
    task.save_to_db()
    return task
