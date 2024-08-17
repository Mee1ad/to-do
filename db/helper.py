from db.models.task import *


def get_task_list_with_id(task_list_id: int):
    return TaskList.select().join(TaskListTask).join(Task).where(TaskList.id == task_list_id).first()
