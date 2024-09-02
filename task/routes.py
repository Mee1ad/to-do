from fasthtml.common import JSONResponse, Div
from pydantic import ValidationError

from app_init import app
from task.components import Task, TaskInput, TaskCheckbox
from task.models import Task
from task.schemas import TaskCreateSchema
from tasklist.models import TaskListTask


@app.post('/task')
def create_task(task_text: str, tasklist_id: int):
    try:
        TaskCreateSchema(task_text=task_text, tasklist_id=tasklist_id)
    except ValidationError as e:
        return JSONResponse({"errors": e.errors()}, status_code=400)
    task = Task.create(title=task_text.capitalize())
    tasklist_task = TaskListTask.create(tasklist_id=tasklist_id, task_id=task.id)
    return (
        Task(task),
    )


@app.put('/task_checkbox')
def update_task(task_id: int):
    query = Task.update(checked=(Task.checked == 0)).where(Task.id == task_id)
    query.execute()
    task = Task.get(id=task_id)


@app.delete('/task/{task_id}')
def delete_task(task_id: int):
    TaskListTask.delete().where(TaskListTask.task == task_id).execute()
    Task.delete().where(Task.id == task_id).execute()


@app.get('/test')
def test():
    return (
        Div(
            Div('Content 1', cls='bg-blue-500 h-40 p-4'),
            Div('Content 2', cls='bg-green-500 h-60 p-4'),
            Div('Content 3', cls='bg-red-500 h-32 p-4'),
            Div('Content 4', cls='bg-yellow-500 h-48 p-4'),
            Div('Content 5', cls='bg-purple-500 h-52 p-4'),
            Div('Content 6', cls='bg-pink-500 h-72 p-4'),
            cls='grid grid-cols-3 gap-4 grid-auto-rows-auto'
        )
    )
