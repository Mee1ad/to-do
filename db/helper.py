from db.models.task import *


def get_task_list_by_id(task_list_id: int):
    return (
        TaskList
        .select()
        .join(TaskListTask)
        .join(Task)
        .where(TaskList.id == task_list_id)
        .first()
    )


def get_space_by_id(space_id: int):
    return (
        Space
        .select()
        .join(SpaceTaskList)
        .join(TaskList)
        .join(TaskListTask)
        .join(Task)
        .where(Space.id == space_id)
        .first()
    )
