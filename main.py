from pydantic import ValidationError

from components.task_components import *
from schemas.task import *

tailwind = Script(src="https://cdn.tailwindcss.com")
app, rt = fast_app(hdrs=(tailwind,), debug=True, live=True, reload_interval=1)


@rt('/')
def get():
    task_list: TaskListSchema = TaskList.select().join(TaskListTask).join(Task).where(TaskList.id == 1).first()
    return (
        task_list_view(task_list)
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


@rt('/task_checkbox')
def put(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)
    return task_checkbox(task)


serve()
