from fasthtml.common import JSONResponse, Div
from pydantic import ValidationError

from app_init import app
from auth.helper import get_user_from_session
from auth.schemas import UserSchema
from space.models import SpaceTaskList
from tasklist.components import TasklistCard, NewTasklistTitle, TasklistTitle
from tasklist.models import TaskList, TaskListTask
from tasklist.schemas import TaskListCreateSchema, TaskListUpdateSchema


@app.post('/tasklist')
def create_tasklist(tasklist_title: str, space_id: int, session):
    user: UserSchema = get_user_from_session(session)
    try:
        TaskListCreateSchema(tasklist_title=tasklist_title, space_id=space_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    tasklist = TaskList.create(title=tasklist_title.capitalize(), user_id=user.id)
    space_tasklist = SpaceTaskList.create(space_id=space_id, tasklist_id=tasklist.id)
    return (
        TasklistCard(tasklist),
        Div(
            NewTasklistTitle(space_id),
            id='new_tasklist_title_component',
        ),)


@app.put('/tasklist/title')
def update_tasklist(tasklist_id: int, tasklist_title: str):
    try:
        TaskListUpdateSchema(id=tasklist_id, title=tasklist_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    updated = TaskList.update(title=tasklist_title.capitalize()).where(TaskList.id == tasklist_id).execute()
    tasklist = TaskList.get(id=tasklist_id)
    if updated:
        return TasklistTitle(tasklist)


@app.delete('/tasklist/{tasklist_id}')
def delete_tasklist(tasklist_id: int):
    TaskListTask.delete().where(TaskListTask.tasklist == tasklist_id).execute()
    SpaceTaskList.delete().where(SpaceTaskList.tasklist == tasklist_id).execute()
    TaskList.delete().where(TaskList.id == tasklist_id).execute()


@app.patch('/tasklist/{tasklist_id}/sort')
def sort_tasks(tasklist_id: int, tasks: list[int]):
    for index, task_id in enumerate(tasks):
        TaskListTask.update(order=index).where(TaskListTask.tasklist == tasklist_id,
                                               TaskListTask.task == task_id).execute()


@app.patch('/tasklist/archive/{tasklist_id}')
def make_archive(session, tasklist_id: int):
    user = get_user_from_session(session)
    updated = TaskList.update(archived=~TaskList.archived).where(TaskList.user_id == user,
                                                                 TaskList.id == tasklist_id).execute()
    if not updated:
        print('not updated')
