from db.models.task import *
from schemas.task import *


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
    space: SpaceSchema = (
        Space
        .select()
        .join(SpaceTaskList, JOIN.LEFT_OUTER)
        .join(TaskList, JOIN.LEFT_OUTER)
        .join(TaskListTask, JOIN.LEFT_OUTER)
        .join(Task, JOIN.LEFT_OUTER)
        .where(Space.id == space_id)
        .first()
    )
    return space
