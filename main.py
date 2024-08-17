from pydantic import ValidationError

from components.task_components import *
from schemas.task import *
from db.helper import *

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=1)


@rt('/')
def get():
    space = get_space_by_id(1)
    return (
        Div(
            space_view(space),

            cls='pt-10 pl-10',
        )

    )


@rt('/add_task')
def post(task_text: str, tasklist_id: int):
    try:
        TaskCreateSchema(task_text=task_text, tasklist_id=tasklist_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task = Task.create(title=task_text)
    tasklist_task = TaskListTask.create(tasklist_id=tasklist_id, task_id=task.id)
    return (
        task_item(task),
        new_task_input_field(tasklist_id)
    )


@rt('/task_list')
def post(task_list_title: str, space_id: int):
    try:
        TaskListCreateSchema(task_list_title=task_list_title, space_id=space_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task_list = TaskList.create(title=task_list_title.capitalize())
    space_task_list = SpaceTaskList.create(space_id=space_id, task_list_id=task_list.id)
    return (
        task_list_view(task_list),
        new_task_list_title_view(task_list.id),
    )


@rt('/task_list')
def put(task_list_id: int, task_list_title: str):
    try:
        TaskListUpdateSchema(id=task_list_id, title=task_list_title)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    TaskList.update(title=task_list_title.capitalize()).where(TaskList.id == task_list_id).execute()
    task_list = TaskList.get(TaskList.id == task_list_id)
    return task_list_title_view(task_list)


@rt('/task_checkbox')
def put(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)
    return task_checkbox(task)


serve()
