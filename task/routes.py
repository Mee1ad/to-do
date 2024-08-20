from fasthtml.common import JSONResponse
from pydantic import ValidationError

from app_init import app
from task.components import task_component, new_task_input_component, task_checkbox_component, add_task_button_component
from task.models import Task
from task.schemas import TaskCreateSchema
from tasklist.models import TaskListTask


@app.post('/task')
def create_task(task_text: str, tasklist_id: int):
    try:
        TaskCreateSchema(task_text=task_text, tasklist_id=tasklist_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task = Task.create(title=task_text)
    tasklist_task = TaskListTask.create(tasklist_id=tasklist_id, task_id=task.id)
    return (
        task_component(task),
        new_task_input_component(tasklist_id)
    )


@app.put('/task_checkbox')
def update_task(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)
    return task_checkbox_component(task)


@app.delete('/task/{task_id}')
def delete_task(task_id: int):
    TaskListTask.delete().where(TaskListTask.task == task_id).execute()
    Task.delete().where(Task.id == task_id).execute()


@app.get('/test')
def test():
    return add_task_button_component()
